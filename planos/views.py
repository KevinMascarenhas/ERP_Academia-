from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_GET, require_http_methods, require_POST

from academia.models import Usuario
from academia.views import get_aluno_from_user, perfil_required

from .models import Plano


@perfil_required(Usuario.PERFIL_ADMIN, Usuario.PERFIL_FUNCIONARIO)
@require_GET
def listar_planos(request):
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
@require_http_methods(["GET", "POST"])
def editar_plano(request, id_plano):
    plano = get_object_or_404(Plano, pk=id_plano)
    if request.method == "POST":
        plano.nome_plano = request.POST.get("nome_plano")
        plano.preco = request.POST.get("preco")
        plano.modalidades_inclusas = request.POST.get("modalidades_inclusas")
        plano.duracao_meses = request.POST.get("duracao_meses")
        plano.save()
        return redirect("listar_planos")
    return render(request, "planos/editar_plano.html", {"usuario": request.user, "plano": plano, "acao": "Editar"})


@perfil_required(Usuario.PERFIL_ADMIN, Usuario.PERFIL_FUNCIONARIO)
@require_POST
def excluir_plano(request, id_plano):
    plano = get_object_or_404(Plano, pk=id_plano)
    plano.delete()
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
