import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_GET, require_http_methods, require_POST

from academia.models import Aluno, Usuario
from academia.views import get_aluno_from_user, perfil_required

from .models import Frequencia, Inscricao, Modalidade


def parse_list_field(raw_value):
    value = (raw_value or "").strip()
    if not value:
        return []
    try:
        parsed = json.loads(value)
        if isinstance(parsed, list):
            return [str(item).strip().strip("\"'") for item in parsed if str(item).strip()]
    except json.JSONDecodeError:
        pass
    value = value.strip("[]")
    return [item.strip().strip("\"'") for item in value.split(",") if item.strip().strip("\"'")]


def normalize_days_value(value):
    if isinstance(value, list):
        return value
    if isinstance(value, str):
        return parse_list_field(value)
    return []


@login_required(login_url="login")
@require_GET
def listar_modalidades(request):
    modalidades = Modalidade.objects.all().order_by("modalidade_nome")
    for modalidade in modalidades:
        modalidade.dias_list = normalize_days_value(modalidade.dias_semana)
        modalidade.dias_display = ", ".join(modalidade.dias_list) if modalidade.dias_list else "-"
    aluno = get_aluno_from_user(request.user)
    modalidades_registradas = aluno.modalidades_inscritas.all() if aluno else []
    registradas_ids = {modalidade.id for modalidade in modalidades_registradas}
    limite_modalidades = aluno.plano.modalidades_inclusas if aluno and aluno.plano else 0
    total_registradas = len(registradas_ids)

    return render(
        request,
        "modalidades/listar_modalidades.html",
        {
            "usuario": request.user,
            "modalidades": modalidades,
            "aluno": aluno,
            "registradas_ids": registradas_ids,
            "limite_modalidades": limite_modalidades,
            "total_registradas": total_registradas,
            "pode_gerenciar": request.user.perfil in {Usuario.PERFIL_ADMIN, Usuario.PERFIL_FUNCIONARIO},
            "pode_registrar": request.user.perfil == Usuario.PERFIL_ALUNO,
        },
    )


@perfil_required(Usuario.PERFIL_ADMIN, Usuario.PERFIL_FUNCIONARIO)
@require_http_methods(["GET", "POST"])
def criar_modalidade(request):
    if request.method == "POST":
        Modalidade.objects.create(
            modalidade_nome=request.POST.get("modalidade_nome"),
            categoria=request.POST.get("categoria"),
            horario=request.POST.get("horario"),
            dias_semana=parse_list_field(request.POST.get("dias_semana")),
        )
        return redirect("listar_modalidades")
    return render(request, "modalidades/criar_modalidade.html", {"usuario": request.user, "acao": "Criar"})


@perfil_required(Usuario.PERFIL_ADMIN, Usuario.PERFIL_FUNCIONARIO)
@require_http_methods(["GET", "POST"])
def editar_modalidade(request, pk):
    modalidade = get_object_or_404(Modalidade, pk=pk)
    if request.method == "POST":
        modalidade.modalidade_nome = request.POST.get("modalidade_nome")
        modalidade.categoria = request.POST.get("categoria")
        modalidade.horario = request.POST.get("horario")
        modalidade.dias_semana = parse_list_field(request.POST.get("dias_semana"))
        modalidade.save()
        return redirect("listar_modalidades")
    modalidade.dias_input = ", ".join(normalize_days_value(modalidade.dias_semana))
    return render(request, "modalidades/editar_modalidade.html", {"usuario": request.user, "modalidade": modalidade, "acao": "Editar"})


@perfil_required(Usuario.PERFIL_ADMIN, Usuario.PERFIL_FUNCIONARIO)
@require_POST
def excluir_modalidade(request, pk):
    modalidade = get_object_or_404(Modalidade, pk=pk)
    modalidade.delete()
    return redirect("listar_modalidades")


@perfil_required(Usuario.PERFIL_ALUNO)
@require_POST
def registrar_modalidade(request, pk):
    aluno = get_aluno_from_user(request.user)
    modalidade = get_object_or_404(Modalidade, pk=pk)

    if not aluno:
        messages.error(request, "Não foi possível localizar o perfil de aluno.")
        return redirect("listar_modalidades")

    if not aluno.plano:
        messages.error(request, "Você precisa estar vinculado a um plano para se registrar em modalidades.")
        return redirect("listar_modalidades")

    total_registradas = aluno.modalidades_inscritas.count()
    if aluno.modalidades_inscritas.filter(pk=modalidade.pk).exists():
        messages.warning(request, "Você já está registrado nessa modalidade.")
        return redirect("listar_modalidades")

    if total_registradas >= aluno.plano.modalidades_inclusas:
        messages.error(request, "Seu plano não permite registrar mais modalidades.")
        return redirect("listar_modalidades")

    aluno.modalidades_inscritas.add(modalidade)
    Inscricao.objects.create(
        aluno=aluno,
        modalidade=modalidade,
        data=timezone.localdate(),
        hora=timezone.now().time().replace(microsecond=0),
        status=Inscricao.STATUS_CONFIRMADO,
    )
    messages.success(request, "Modalidade registrada com sucesso.")
    return redirect("listar_modalidades")


@perfil_required(Usuario.PERFIL_ALUNO)
@require_POST
def cancelar_registro_modalidade(request, pk):
    aluno = get_aluno_from_user(request.user)
    modalidade = get_object_or_404(Modalidade, pk=pk)

    if not aluno or not aluno.modalidades_inscritas.filter(pk=modalidade.pk).exists():
        messages.error(request, "Você não está registrado nessa modalidade.")
        return redirect("listar_modalidades")

    aluno.modalidades_inscritas.remove(modalidade)
    inscricao = (
        Inscricao.objects.filter(aluno=aluno, modalidade=modalidade, status=Inscricao.STATUS_CONFIRMADO)
        .order_by("-id")
        .first()
    )
    if inscricao:
        inscricao.cancelar()
    messages.success(request, "Registro cancelado com sucesso.")
    return redirect("listar_modalidades")


@login_required(login_url="login")
@require_GET
def listar_frequencias(request):
    aluno = get_aluno_from_user(request.user)
    frequencias = Frequencia.objects.select_related("aluno", "modalidade")
    if request.user.perfil == Usuario.PERFIL_ALUNO and aluno:
        frequencias = frequencias.filter(aluno=aluno)

    return render(
        request,
        "modalidades/listar_frequencias.html",
        {
            "usuario": request.user,
            "frequencias": frequencias.order_by("-data", "-hora"),
            "pode_gerenciar": request.user.perfil in {Usuario.PERFIL_ADMIN, Usuario.PERFIL_FUNCIONARIO},
        },
    )


@perfil_required(Usuario.PERFIL_ADMIN, Usuario.PERFIL_FUNCIONARIO)
@require_http_methods(["GET", "POST"])
def criar_frequencia(request):
    if request.method == "POST":
        Frequencia.objects.create(
            aluno_id=request.POST.get("aluno_id"),
            modalidade_id=request.POST.get("modalidade_id"),
            data=request.POST.get("data") or None,
            hora=request.POST.get("hora") or None,
        )
        return redirect("listar_frequencias")
    return render(
        request,
        "modalidades/criar_frequencia.html",
        {
            "usuario": request.user,
            "alunos": Aluno.objects.order_by("nome"),
            "modalidades": Modalidade.objects.order_by("modalidade_nome"),
        },
    )


@perfil_required(Usuario.PERFIL_ADMIN, Usuario.PERFIL_FUNCIONARIO)
@require_http_methods(["GET", "POST"])
def editar_frequencia(request, pk):
    frequencia = get_object_or_404(Frequencia, pk=pk)
    if request.method == "POST":
        frequencia.aluno_id = request.POST.get("aluno_id")
        frequencia.modalidade_id = request.POST.get("modalidade_id")
        frequencia.data = request.POST.get("data") or None
        frequencia.hora = request.POST.get("hora") or None
        frequencia.save()
        return redirect("listar_frequencias")
    return render(
        request,
        "modalidades/editar_frequencia.html",
        {
            "usuario": request.user,
            "frequencia": frequencia,
            "alunos": Aluno.objects.order_by("nome"),
            "modalidades": Modalidade.objects.order_by("modalidade_nome"),
        },
    )


@perfil_required(Usuario.PERFIL_ADMIN, Usuario.PERFIL_FUNCIONARIO)
@require_POST
def excluir_frequencia(request, pk):
    frequencia = get_object_or_404(Frequencia, pk=pk)
    frequencia.delete()
    return redirect("listar_frequencias")
