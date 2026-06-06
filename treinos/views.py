import json

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_GET, require_http_methods, require_POST

from academia.models import Aluno, Usuario
from academia.views import get_aluno_from_user, perfil_required

from .models import Treino


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


@login_required(login_url="login")
@require_GET
def listar_treinos(request):
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
@require_http_methods(["GET", "POST"])
def editar_treino(request, id_treino):
    treino = get_object_or_404(Treino, pk=id_treino)
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
@require_POST
def excluir_treino(request, id_treino):
    treino = get_object_or_404(Treino, pk=id_treino)
    treino.delete()
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
