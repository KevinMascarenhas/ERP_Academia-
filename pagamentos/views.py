import json

from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_GET, require_http_methods, require_POST
from drf_spectacular.utils import extend_schema
from django.utils.dateparse import parse_date
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from academia.models import Aluno, Usuario
from academia.views import perfil_required
from academia.permissions import IsAdminOrFuncionarioProfile

from .models import Pagamento
from .serializers import PagamentoSerializer


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
    summary="Lista todos os pagamentos",
    responses={200: PagamentoSerializer(many=True)},
    tags=["Pagamentos"],
)
@extend_schema(
    methods=["POST"],
    summary="Cria um novo pagamento",
    request=PagamentoSerializer,
    responses={201: PagamentoSerializer},
    tags=["Pagamentos"],
)
@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated, IsAdminOrFuncionarioProfile])
def pagamentos_list_api(request):
    if request.method == "POST":
        serializer = PagamentoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    pagamentos = Pagamento.objects.select_related("aluno").all()
    return Response(PagamentoSerializer(pagamentos, many=True).data)


@extend_schema(
    methods=["GET"],
    summary="Retorna detalhes de um pagamento",
    responses={200: PagamentoSerializer},
    tags=["Pagamentos"],
)
@extend_schema(
    methods=["PUT"],
    summary="Atualiza um pagamento (completo)",
    request=PagamentoSerializer,
    responses={200: PagamentoSerializer},
    tags=["Pagamentos"],
)
@extend_schema(
    methods=["PATCH"],
    summary="Atualiza um pagamento (parcial)",
    request=PagamentoSerializer,
    responses={200: PagamentoSerializer},
    tags=["Pagamentos"],
)
@extend_schema(
    methods=["DELETE"],
    summary="Remove um pagamento",
    responses={204: None},
    tags=["Pagamentos"],
)
@api_view(["GET", "PUT", "PATCH", "DELETE"])
@permission_classes([IsAuthenticated, IsAdminOrFuncionarioProfile])
def pagamentos_detail_api(request, pagamento_id):
    pagamento = get_object_or_404(Pagamento, id=pagamento_id)
    if request.method == "GET":
        return Response(PagamentoSerializer(pagamento).data)
    if request.method == "DELETE":
        pagamento.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    serializer = PagamentoSerializer(pagamento, data=request.data, partial=request.method == "PATCH")
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# --- HTML views (templates) ---

@perfil_required(Usuario.PERFIL_ADMIN, Usuario.PERFIL_FUNCIONARIO)
@require_http_methods(["GET", "POST"])
def listar_pagamentos(request):
    if request.method == "POST":
        serializer = PagamentoSerializer(data=get_json_data(request))
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

    pagamentos = Pagamento.objects.select_related("aluno").all()
    return render(request, "pagamentos/listar_pagamentos.html", {"usuario": request.user, "pagamentos": pagamentos})


@perfil_required(Usuario.PERFIL_ADMIN, Usuario.PERFIL_FUNCIONARIO)
@require_http_methods(["GET", "POST"])
def criar_pagamento(request):
    if request.method == "POST":
        Pagamento.objects.create(
            aluno_id=request.POST.get("aluno_id"),
            valor=request.POST.get("valor"),
            mes_ano=request.POST.get("mes_ano"),
            status=request.POST.get("status"),
        )
        return redirect("listar_pagamentos")
    return render(
        request,
        "pagamentos/criar_pagamento.html",
        {"usuario": request.user, "alunos": Aluno.objects.order_by("nome"), "acao": "Criar"},
    )


@perfil_required(Usuario.PERFIL_ADMIN, Usuario.PERFIL_FUNCIONARIO)
@require_http_methods(["GET", "POST", "PUT", "PATCH", "DELETE"])
def editar_pagamento(request, pagamento_id):
    pagamento = get_object_or_404(Pagamento, id=pagamento_id)
    if request.method == "DELETE":
        pagamento.delete()
        return HttpResponse(status=204)
    if request.method in {"PUT", "PATCH"}:
        serializer = PagamentoSerializer(pagamento, data=get_json_data(request), partial=request.method == "PATCH")
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)
    if request.method == "POST":
        pagamento.aluno_id = request.POST.get("aluno_id")
        pagamento.valor = request.POST.get("valor")
        pagamento.mes_ano = request.POST.get("mes_ano")
        pagamento.status = request.POST.get("status")
        pagamento.save()
        return redirect("listar_pagamentos")
    return render(
        request,
        "pagamentos/editar_pagamento.html",
        {"usuario": request.user, "pagamento": pagamento, "alunos": Aluno.objects.order_by("nome"), "acao": "Editar"},
    )


@perfil_required(Usuario.PERFIL_ADMIN, Usuario.PERFIL_FUNCIONARIO)
@require_http_methods(["POST", "DELETE"])
def excluir_pagamento(request, pagamento_id):
    pagamento = get_object_or_404(Pagamento, id=pagamento_id)
    pagamento.delete()
    if request.method == "DELETE":
        return HttpResponse(status=204)
    return redirect("listar_pagamentos")
