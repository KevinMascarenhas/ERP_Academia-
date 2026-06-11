from django.contrib.auth.decorators import login_required
import json

from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_GET, require_http_methods, require_POST
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from academia.models import Usuario
from academia.views import get_aluno_from_user, perfil_required

from .models import Plano
from academia.permissions import IsAdminOrFuncionarioProfile
from .serializers import PlanoSerializer


def get_json_data(request):
    if not request.body:
        return {}
    try:
        return json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        return {}


# --- REST API views (visíveis no Swagger) ---

@extend_schema(
    methods=["GET"],
    summary="Lista todos os planos",
    responses={200: PlanoSerializer(many=True)},
    tags=["Planos"],
)
@extend_schema(
    methods=["POST"],
    summary="Cria um novo plano",
    request=PlanoSerializer,
    responses={201: PlanoSerializer},
    tags=["Planos"],
)
@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated, IsAdminOrFuncionarioProfile])
def planos_list_api(request):
    if request.method == "POST":
        serializer = PlanoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    planos = Plano.objects.all().order_by("id_plano")
    return Response(PlanoSerializer(planos, many=True).data)


@extend_schema(
    methods=["GET"],
    summary="Retorna detalhes de um plano",
    responses={200: PlanoSerializer},
    tags=["Planos"],
)
@extend_schema(
    methods=["PUT"],
    summary="Atualiza um plano (completo)",
    request=PlanoSerializer,
    responses={200: PlanoSerializer},
    tags=["Planos"],
)
@extend_schema(
    methods=["PATCH"],
    summary="Atualiza um plano (parcial)",
    request=PlanoSerializer,
    responses={200: PlanoSerializer},
    tags=["Planos"],
)
@extend_schema(
    methods=["DELETE"],
    summary="Remove um plano",
    responses={204: None},
    tags=["Planos"],
)
@api_view(["GET", "PUT", "PATCH", "DELETE"])
@permission_classes([IsAuthenticated, IsAdminOrFuncionarioProfile])
def planos_detail_api(request, id_plano):
    plano = get_object_or_404(Plano, pk=id_plano)
    if request.method == "GET":
        return Response(PlanoSerializer(plano).data)
    if request.method == "DELETE":
        plano.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    serializer = PlanoSerializer(plano, data=request.data, partial=request.method == "PATCH")
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# --- HTML views (templates) ---

@perfil_required(Usuario.PERFIL_ADMIN, Usuario.PERFIL_FUNCIONARIO)
@require_http_methods(["GET", "POST"])
def listar_planos(request):
    if request.method == "POST":
        serializer = PlanoSerializer(data=get_json_data(request))
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

    planos = Plano.objects.all().order_by("id_plano")
    return render(
        request,
        "planos/listar_planos.html",
        {
            "usuario": request.user,
            "planos": planos,
            "pode_gerenciar": True,
        },
    )


@perfil_required(Usuario.PERFIL_ADMIN, Usuario.PERFIL_FUNCIONARIO)
@require_http_methods(["GET", "POST"])
def criar_plano(request):
    if request.method == "POST":
        Plano.objects.create(
            nome_plano=request.POST.get("nome_plano"),
            preco=request.POST.get("preco"),
            modalidades_inclusas=request.POST.get("modalidades_inclusas"),
            duracao_meses=request.POST.get("duracao_meses"),
        )
        return redirect("listar_planos")
    return render(request, "planos/criar_plano.html", {"usuario": request.user, "acao": "Criar"})


@perfil_required(Usuario.PERFIL_ADMIN, Usuario.PERFIL_FUNCIONARIO)
@require_http_methods(["GET", "POST", "PUT", "PATCH", "DELETE"])
def editar_plano(request, id_plano):
    plano = get_object_or_404(Plano, pk=id_plano)
    if request.method == "DELETE":
        plano.delete()
        return HttpResponse(status=204)
    if request.method in {"PUT", "PATCH"}:
        serializer = PlanoSerializer(plano, data=get_json_data(request), partial=request.method == "PATCH")
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)
    if request.method == "POST":
        plano.nome_plano = request.POST.get("nome_plano")
        plano.preco = request.POST.get("preco")
        plano.modalidades_inclusas = request.POST.get("modalidades_inclusas")
        plano.duracao_meses = request.POST.get("duracao_meses")
        plano.save()
        return redirect("listar_planos")
    return render(request, "planos/editar_plano.html", {"usuario": request.user, "plano": plano, "acao": "Editar"})


@perfil_required(Usuario.PERFIL_ADMIN, Usuario.PERFIL_FUNCIONARIO)
@require_http_methods(["POST", "DELETE"])
def excluir_plano(request, id_plano):
    plano = get_object_or_404(Plano, pk=id_plano)
    plano.delete()
    if request.method == "DELETE":
        return HttpResponse(status=204)
    return redirect("listar_planos")


@login_required(login_url="login")
@require_GET
def meu_plano(request):
    aluno = get_aluno_from_user(request.user)
    if request.user.perfil != Usuario.PERFIL_ALUNO:
        return redirect("listar_planos")
    return render(
        request,
        "planos/meu_plano.html",
        {
            "usuario": request.user,
            "aluno": aluno,
            "plano": aluno.plano if aluno else None,
        },
    )
