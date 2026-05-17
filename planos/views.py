from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, require_http_methods, require_GET, require_POST
from academia.models import perfil_required
from .models import Plano 

@login_required(login_url="login")
@require_GET
def listar_planos(request):
    planos = Plano.objects.all()
    return render(request, "planos/listar_planos.html", {"planos": planos})

@perfil_required("Administrador")
@require_http_methods(["GET", "POST"])
def criar_plano(request):
    if request.method == "POST":
        Plano.objects.create(
            nome_plano = request.POST.get("nome_plano"),
            preco = request.POST.get("preco"),
            modalidades_inclusas = request.POST.get("modalidades_inclusas"),
            duracao_meses = request.POST.get("duracao_meses")
        )
        return redirect("listar_planos")
    return render(request, "planos/criar_plano.html", {"planos": Plano.objects.all(), "acao": "Criar"})

@perfil_required("Administrador")
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
    return render(request, "planos/editar_plano.html", {"plano": plano, "acao": "Editar"})

@perfil_required("Administrador")
@require_POST
def excluir_plano(request, id_plano):
    plano = get_object_or_404(Plano, pk=id_plano)
    if request.method == "POST":
        plano.delete()
        return redirect("listar_planos")
    return render(request, "planos/excluir_plano.html", {"plano": plano})


