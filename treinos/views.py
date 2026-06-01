from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_GET, require_POST
from academia.views import perfil_required
from .models import Treino

@login_required(login_url="login")
@require_GET
def listar_treinos(request):
    treinos = Treino.objects.all()
    return render(request, "treinos/listar_treinos.html", {"treinos": treinos})

@perfil_required("Administrador")
@require_http_methods(["GET", "POST"])
def criar_treino(request):
    if request.method == "POST":
        Treino.objects.create(
            nome_treino = request.POST.get("nome_treino"),
            descricao = request.POST.get("descricao"),
            aluno_id = request.POST.get("aluno_id"),
            grupo_muscular = request.POST.get("grupo_muscular"),
            exercicios = request.POST.get("exercicios"),
            series = request.POST.get("series"),
            repeticoes = request.POST.get("repeticoes"),
            data = request.POST.get("data")
        )
        return redirect("listar_treinos")
    return render(request, "treinos/criar_treino.html", {"treinos": Treino.objects.all(), "acao": "Criar"})

@perfil_required("Administrador")
@require_http_methods(["GET", "POST"])
def editar_treino(request, id_treino):
    treino = get_object_or_404(Treino, pk=id_treino)
    if request.method == "POST":
        treino.nome_treino = request.POST.get("nome_treino")
        treino.descricao = request.POST.get("descricao")
        treino.aluno_id = request.POST.get("aluno_id")
        treino.grupo_muscular = request.POST.get("grupo_muscular")
        treino.exercicios = request.POST.get("exercicios")
        treino.series = request.POST.get("series")
        treino.repeticoes = request.POST.get("repeticoes")
        treino.data = request.POST.get("data")
        treino.save()
        return redirect("listar_treinos")
    return render(request, "treinos/editar_treino.html", {"treino": treino, "acao": "Editar"})

@perfil_required("Administrador")
@require_POST
def excluir_treino(request, id_treino):
    treino = get_object_or_404(Treino, pk=id_treino)
    if request.method == "POST":
        treino.delete()
        return redirect("listar_treinos")
    return render(request, "treinos/excluir_treino.html", {"treino": treino})


