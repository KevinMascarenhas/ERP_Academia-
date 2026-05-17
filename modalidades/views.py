from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, require_http_methods, require_GET, require_POST
from academia.models import perfil_required
from .models import Modalidade

@login_required(login_url="login")
@require_GET
def listar_modalidades(request):
    modalidades = Modalidade.objects.all()
    return render(request, "modalidades/listar_modalidades.html", {"modalidades": modalidades})

@perfil_required("Administrador")
@require_http_methods(["GET", "POST"])
def criar_modalidade(request):
    if request.method == "POST":
        Modalidade.objects.create(
            modalidade_nome = request.POST.get("modalidade_nome"),
            categoria = request.POST.get("categoria"),
            horario = request.POST.get("horario"),
            dias_semana = request.POST.get("dias_semana")
        )
        return redirect("modalidades/listar_modalidades")
    return render(request, "modalidades/criar_modalidade.html", {"modalidades": Modalidade.objects.all(), "acao": "Criar"})

@perfil_required("Administrador")
@require_http_methods(["GET", "POST"])
def editar_modalidade(request, pk):
    modalidade = get_object_or_404(Modalidade, pk=pk)
    if request.method == "POST":
        modalidade.modalidade_nome = request.POST.get("modalidade_nome")
        modalidade.categoria = request.POST.get("categoria"),
        modalidade.horario = request.POST.get("horario"),
        modalidade.dias_semana = request.POST.get("dias_semana")
        return redirect("listar_modalidades")
    return render(request, "modalidades/editar_modalidade.html", {"modalidade": modalidade, "acao": "Editar"})

@perfil_required("Administrador")
@require_POST
def excluir_modalidade(request, pk):
    modalidade = get_object_or_404(Modalidade, pk=pk)
    if request.method == "POST":
        modalidade.delete()
        return redirect("listar_modalidades")
    return render(request, "planos/excluir_modalidade.html", {"modalidade": modalidade})


        


