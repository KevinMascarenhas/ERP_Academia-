import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from academia.models import Aluno, Usuario
from academia.views import get_aluno_from_user, perfil_required
from academia.permissions import IsAdminOrFuncionarioProfile

from .models import Treino
from .serializers import SugestaoTreinoSerializer, TreinoSerializer


def get_json_data(request):
    if not request.body:
        return {}
    try:
        return json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        return {}


def parse_json_or_list(raw_value):
    value = (raw_value or "").strip()
    if not value:
        return []
    try:
        parsed = json.loads(value)
        if isinstance(parsed, list):
            return parsed
    except json.JSONDecodeError:
        pass
    return [item.strip() for item in value.split(",") if item.strip()]


def sugestoes_por_grupo():
    return {
        "Peito": ["Supino reto", "Supino inclinado", "Crucifixo", "Crossover"],
        "Costas": ["Puxada frontal", "Remada curvada", "Remada unilateral", "Pulldown"],
        "Pernas": ["Agachamento", "Leg press", "Cadeira extensora", "Cadeira flexora"],
        "Ombro": ["Desenvolvimento com halteres", "Elevacao lateral", "Elevacao frontal", "Encolhimento"],
        "Biceps": ["Rosca direta", "Rosca alternada", "Rosca concentrada", "Rosca martelo"],
        "Triceps": ["Triceps testa", "Triceps pulley", "Triceps frances", "Mergulho no banco"],
        "Abdomen": ["Abdominal crunch", "Prancha", "Abdominal obliquo", "Elevacao de pernas"],
    }


# --- REST API views (visíveis no Swagger) ---

@extend_schema(
    methods=["GET"],
    summary="Lista todos os treinos",
    responses={200: TreinoSerializer(many=True)},
    tags=["Treinos"],
)
@extend_schema(
    methods=["POST"],
    summary="Cria um novo treino",
    request=TreinoSerializer,
    responses={201: TreinoSerializer},
    tags=["Treinos"],
)
@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def treinos_list_api(request):
    if request.method == "POST":
        serializer = TreinoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    aluno = get_aluno_from_user(request.user)
    treinos = Treino.objects.select_related("aluno")
    if request.user.perfil == Usuario.PERFIL_ALUNO and aluno:
        treinos = treinos.filter(aluno=aluno)
    return Response(TreinoSerializer(treinos.order_by("-data"), many=True).data)


@extend_schema(
    methods=["GET"],
    summary="Retorna detalhes de um treino",
    responses={200: TreinoSerializer},
    tags=["Treinos"],
)
@extend_schema(
    methods=["PUT"],
    summary="Atualiza um treino (completo)",
    request=TreinoSerializer,
    responses={200: TreinoSerializer},
    tags=["Treinos"],
)
@extend_schema(
    methods=["PATCH"],
    summary="Atualiza um treino (parcial)",
    request=TreinoSerializer,
    responses={200: TreinoSerializer},
    tags=["Treinos"],
)
@extend_schema(
    methods=["DELETE"],
    summary="Remove um treino",
    responses={204: None},
    tags=["Treinos"],
)
@api_view(["GET", "PUT", "PATCH", "DELETE"])
@permission_classes([IsAuthenticated, IsAdminOrFuncionarioProfile])
def treinos_detail_api(request, id_treino):
    treino = get_object_or_404(Treino, pk=id_treino)
    if request.method == "GET":
        return Response(TreinoSerializer(treino).data)
    if request.method == "DELETE":
        treino.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    serializer = TreinoSerializer(treino, data=request.data, partial=request.method == "PATCH")
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# --- HTML views (templates) ---
@login_required(login_url="login")
@require_http_methods(["GET", "POST"])
def listar_treinos(request):
    if request.method == "POST":
        serializer = TreinoSerializer(data=get_json_data(request))
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

    aluno = get_aluno_from_user(request.user)
    treinos = Treino.objects.select_related("aluno")
    if request.user.perfil == Usuario.PERFIL_ALUNO and aluno:
        treinos = treinos.filter(aluno=aluno)
    return render(
        request,
        "treinos/listar_treinos.html",
        {
            "usuario": request.user,
            "treinos": treinos.order_by("-data"),
            "pode_gerenciar": request.user.perfil in {Usuario.PERFIL_ADMIN, Usuario.PERFIL_FUNCIONARIO},
        },
    )


@perfil_required(Usuario.PERFIL_ADMIN, Usuario.PERFIL_FUNCIONARIO)
@require_http_methods(["GET", "POST"])
def criar_treino(request):
    if request.method == "POST":
        Treino.objects.create(
            nome_treino=request.POST.get("nome_treino"),
            descricao=request.POST.get("descricao"),
            aluno_id=request.POST.get("aluno_id"),
            grupo_muscular=request.POST.get("grupo_muscular"),
            exercicios=parse_json_or_list(request.POST.get("exercicios")),
            series=request.POST.get("series"),
            repeticoes=request.POST.get("repeticoes"),
            data=request.POST.get("data"),
        )
        return redirect("listar_treinos")
    return render(
        request,
        "treinos/criar_treino.html",
        {"usuario": request.user, "acao": "Criar", "alunos": Aluno.objects.order_by("nome")},
    )


@perfil_required(Usuario.PERFIL_ADMIN, Usuario.PERFIL_FUNCIONARIO)
@require_http_methods(["GET", "POST", "PUT", "PATCH", "DELETE"])
def editar_treino(request, id_treino):
    treino = get_object_or_404(Treino, pk=id_treino)
    if request.method == "DELETE":
        treino.delete()
        return HttpResponse(status=204)
    if request.method in {"PUT", "PATCH"}:
        serializer = TreinoSerializer(treino, data=get_json_data(request), partial=request.method == "PATCH")
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)
    if request.method == "POST":
        treino.nome_treino = request.POST.get("nome_treino")
        treino.descricao = request.POST.get("descricao")
        treino.aluno_id = request.POST.get("aluno_id")
        treino.grupo_muscular = request.POST.get("grupo_muscular")
        treino.exercicios = parse_json_or_list(request.POST.get("exercicios"))
        treino.series = request.POST.get("series")
        treino.repeticoes = request.POST.get("repeticoes")
        treino.data = request.POST.get("data")
        treino.save()
        return redirect("listar_treinos")
    return render(
        request,
        "treinos/editar_treino.html",
        {
            "usuario": request.user,
            "treino": treino,
            "acao": "Editar",
            "alunos": Aluno.objects.order_by("nome"),
        },
    )


@perfil_required(Usuario.PERFIL_ADMIN, Usuario.PERFIL_FUNCIONARIO)
@require_http_methods(["POST", "DELETE"])
def excluir_treino(request, id_treino):
    treino = get_object_or_404(Treino, pk=id_treino)
    treino.delete()
    if request.method == "DELETE":
        return HttpResponse(status=204)
    return redirect("listar_treinos")


@login_required(login_url="login")
@require_http_methods(["GET", "POST"])
def sugerir_treino(request):
    grupo = request.GET.get("grupo", "").strip() if request.method == "GET" else request.POST.get("grupo", "").strip()
    sugestoes = sugestoes_por_grupo()
    exercicios = []
    for chave, lista_exercicios in sugestoes.items():
        if chave.lower() == grupo.lower():
            exercicios = lista_exercicios
            break

    return render(
        request,
        "treinos/sugerir_treino.html",
        {
            "usuario": request.user,
            "grupo": grupo,
            "grupos_disponiveis": list(sugestoes.keys()),
            "exercicios": exercicios,
        },
    )


