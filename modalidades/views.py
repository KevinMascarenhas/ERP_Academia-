import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_GET, require_http_methods, require_POST
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from academia.models import Aluno, Usuario
from academia.views import get_aluno_from_user, perfil_required
from academia.permissions import IsAdminOrFuncionarioProfile

from .models import Frequencia, Inscricao, Modalidade, Turma
from .serializers import FrequenciaSerializer, InscricaoSerializer, ModalidadeSerializer, TurmaSerializer


def get_json_data(request):
    if not request.body:
        return {}
    try:
        return json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        return {}


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


def ensure_turma_for_modalidade(modalidade):
    turma, _ = Turma.objects.get_or_create(
        modalidade=modalidade,
        defaults={"nome": f"Turma {modalidade.modalidade_nome}"},
    )
    return turma


def get_confirmed_inscricao(aluno, modalidade):
    return (
        Inscricao.objects.filter(aluno=aluno, modalidade=modalidade, status=Inscricao.STATUS_CONFIRMADO)
        .order_by("-id")
        .first()
    )


def get_turma_context():
    turmas = []
    for modalidade in Modalidade.objects.select_related("turma").order_by("modalidade_nome"):
        turma = ensure_turma_for_modalidade(modalidade)
        turma.inscricoes_confirmadas = list(
            Inscricao.objects.select_related("aluno", "modalidade")
            .filter(modalidade=modalidade, status=Inscricao.STATUS_CONFIRMADO)
            .order_by("aluno__nome")
        )
        turma.total_inscritos = len(turma.inscricoes_confirmadas)
        turmas.append(turma)
    return turmas


# REST API views (visíveis no Swagger) 

@extend_schema(
    methods=["GET"],
    summary="Lista todas as modalidades",
    responses={200: ModalidadeSerializer(many=True)},
    tags=["Modalidades"],
)
@extend_schema(
    methods=["POST"],
    summary="Cria uma nova modalidade",
    request=ModalidadeSerializer,
    responses={201: ModalidadeSerializer},
    tags=["Modalidades"],
)
@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def modalidades_list_api(request):
    if request.method == "POST":
        serializer = ModalidadeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    modalidades = Modalidade.objects.all().order_by("modalidade_nome")
    return Response(ModalidadeSerializer(modalidades, many=True).data)


@extend_schema(
    methods=["GET"],
    summary="Retorna detalhes de uma modalidade",
    responses={200: ModalidadeSerializer},
    tags=["Modalidades"],
)
@extend_schema(
    methods=["PUT"],
    summary="Atualiza uma modalidade (completo)",
    request=ModalidadeSerializer,
    responses={200: ModalidadeSerializer},
    tags=["Modalidades"],
)
@extend_schema(
    methods=["PATCH"],
    summary="Atualiza uma modalidade (parcial)",
    request=ModalidadeSerializer,
    responses={200: ModalidadeSerializer},
    tags=["Modalidades"],
)
@extend_schema(
    methods=["DELETE"],
    summary="Remove uma modalidade",
    responses={204: None},
    tags=["Modalidades"],
)
@api_view(["GET", "PUT", "PATCH", "DELETE"])
@permission_classes([IsAuthenticated, IsAdminOrFuncionarioProfile])
def modalidades_detail_api(request, pk):
    modalidade = get_object_or_404(Modalidade, pk=pk)
    if request.method == "GET":
        return Response(ModalidadeSerializer(modalidade).data)
    if request.method == "DELETE":
        modalidade.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    serializer = ModalidadeSerializer(modalidade, data=request.data, partial=request.method == "PATCH")
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    methods=["POST"],
    summary="Cria uma inscrição em modalidade",
    request=InscricaoSerializer,
    responses={201: InscricaoSerializer},
    tags=["Inscrições"],
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def criar_inscricao_api(request):
    serializer = InscricaoSerializer(data=request.data)
    if serializer.is_valid():
        aluno = get_aluno_from_user(request.user)
        modalidade = serializer.validated_data["modalidade"]
        if not aluno or serializer.validated_data["aluno"] != aluno:
            return Response({"detail": "Aluno inválido para o usuário logado."}, status=status.HTTP_403_FORBIDDEN)
        if not aluno.plano:
            return Response({"detail": "Você precisa estar vinculado a um plano."}, status=status.HTTP_400_BAD_REQUEST)
        if aluno.modalidades_inscritas.filter(pk=modalidade.pk).exists():
            return Response({"detail": "Você já está registrado nessa modalidade."}, status=status.HTTP_400_BAD_REQUEST)
        if aluno.modalidades_inscritas.count() >= aluno.plano.modalidades_inclusas:
            return Response({"detail": "Seu plano não permite registrar mais modalidades."}, status=status.HTTP_400_BAD_REQUEST)
        inscricao = serializer.save(status=Inscricao.STATUS_CONFIRMADO)
        inscricao.confirmar()
        return Response(InscricaoSerializer(inscricao).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    methods=["DELETE"],
    summary="Cancela uma inscrição em modalidade",
    responses={200: InscricaoSerializer},
    tags=["Inscrições"],
)
@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def cancelar_inscricao_api(request, pk):
    inscricao = get_object_or_404(Inscricao, pk=pk, status=Inscricao.STATUS_CONFIRMADO)
    inscricao.cancelar()
    return Response(InscricaoSerializer(inscricao).data)


@extend_schema(
    methods=["GET"],
    summary="Lista todas as frequências",
    responses={200: FrequenciaSerializer(many=True)},
    tags=["Frequências"],
)
@extend_schema(
    methods=["POST"],
    summary="Registra uma nova frequência",
    request=FrequenciaSerializer,
    responses={201: FrequenciaSerializer},
    tags=["Frequências"],
)
@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def frequencias_list_api(request):
    if request.method == "POST":
        serializer = FrequenciaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    aluno = get_aluno_from_user(request.user)
    frequencias = Frequencia.objects.select_related("aluno", "modalidade")
    if request.user.perfil == Usuario.PERFIL_ALUNO and aluno:
        frequencias = frequencias.filter(aluno=aluno)
    return Response(FrequenciaSerializer(frequencias.order_by("-data", "-hora"), many=True).data)


@extend_schema(
    methods=["GET"],
    summary="Retorna detalhes de uma frequência",
    responses={200: FrequenciaSerializer},
    tags=["Frequências"],
)
@extend_schema(
    methods=["PUT"],
    summary="Atualiza uma frequência (completo)",
    request=FrequenciaSerializer,
    responses={200: FrequenciaSerializer},
    tags=["Frequências"],
)
@extend_schema(
    methods=["PATCH"],
    summary="Atualiza uma frequência (parcial)",
    request=FrequenciaSerializer,
    responses={200: FrequenciaSerializer},
    tags=["Frequências"],
)
@extend_schema(
    methods=["DELETE"],
    summary="Remove uma frequência",
    responses={204: None},
    tags=["Frequências"],
)
@api_view(["GET", "PUT", "PATCH", "DELETE"])
@permission_classes([IsAuthenticated, IsAdminOrFuncionarioProfile])
def frequencias_detail_api(request, pk):
    frequencia = get_object_or_404(Frequencia, pk=pk)
    if request.method == "GET":
        return Response(FrequenciaSerializer(frequencia).data)
    if request.method == "DELETE":
        frequencia.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    serializer = FrequenciaSerializer(frequencia, data=request.data, partial=request.method == "PATCH")
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# --- HTML views (templates) ---
@require_http_methods(["GET", "POST"])
def listar_modalidades(request):
    if request.method == "POST":
        serializer = ModalidadeSerializer(data=get_json_data(request))
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

    modalidades = Modalidade.objects.all().order_by("modalidade_nome")
    for modalidade in modalidades:
        modalidade.dias_list = normalize_days_value(modalidade.dias_semana)
        modalidade.dias_display = ", ".join(modalidade.dias_list) if modalidade.dias_list else "-"
    aluno = get_aluno_from_user(request.user)
    modalidades_registradas = aluno.modalidades_inscritas.all() if aluno else []
    registradas_ids = {modalidade.id for modalidade in modalidades_registradas}
    inscricoes_por_modalidade = {}
    if aluno:
        inscricoes_por_modalidade = {
            inscricao.modalidade_id: inscricao.id
            for inscricao in Inscricao.objects.filter(aluno=aluno, status=Inscricao.STATUS_CONFIRMADO)
        }
    for modalidade in modalidades:
        modalidade.inscricao_id = inscricoes_por_modalidade.get(modalidade.id)
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
            "inscricoes_por_modalidade": inscricoes_por_modalidade,
            "limite_modalidades": limite_modalidades,
            "total_registradas": total_registradas,
            "hoje": timezone.localdate(),
            "agora": timezone.localtime().time().replace(microsecond=0),
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
@require_http_methods(["GET", "POST", "PUT", "PATCH", "DELETE"])
def editar_modalidade(request, pk):
    modalidade = get_object_or_404(Modalidade, pk=pk)
    if request.method == "DELETE":
        modalidade.delete()
        return HttpResponse(status=204)
    if request.method in {"PUT", "PATCH"}:
        serializer = ModalidadeSerializer(modalidade, data=get_json_data(request), partial=request.method == "PATCH")
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)
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
@require_http_methods(["POST", "DELETE"])
def excluir_modalidade(request, pk):
    modalidade = get_object_or_404(Modalidade, pk=pk)
    modalidade.delete()
    if request.method == "DELETE":
        return HttpResponse(status=204)
    return redirect("listar_modalidades")


@perfil_required(Usuario.PERFIL_ADMIN, Usuario.PERFIL_FUNCIONARIO)
@require_http_methods(["GET"])
def listar_turmas(request):
    alunos = Aluno.objects.filter(is_active=True).order_by("nome")
    turmas = get_turma_context()
    for turma in turmas:
        turma.alunos_disponiveis = alunos
    return render(
        request,
        "modalidades/listar_turmas.html",
        {
            "usuario": request.user,
            "turmas": turmas,
            "alunos": alunos,
            "pode_gerenciar": True,
        },
    )


@extend_schema(
    methods=["GET"],
    summary="Lista as turmas de todas as modalidades",
    responses={200: TurmaSerializer(many=True)},
    tags=["Turmas"],
)
@api_view(["GET"])
@permission_classes([IsAuthenticated, IsAdminOrFuncionarioProfile])
def turmas_list_api(request):
    turmas = get_turma_context()
    return Response(TurmaSerializer(turmas, many=True).data)


@extend_schema(
    methods=["POST"],
    summary="Inscreve um aluno em uma turma",
    request=TurmaSerializer,
    responses={201: InscricaoSerializer},
    tags=["Turmas"],
)
@api_view(["POST"])
@permission_classes([IsAuthenticated, IsAdminOrFuncionarioProfile])
def inscrever_aluno_turma_api(request, turma_id):
    turma = get_object_or_404(Turma, pk=turma_id)
    aluno_id = request.data.get("aluno")
    aluno = get_object_or_404(Aluno, pk=aluno_id)
    inscritos_atuais = Inscricao.objects.filter(modalidade=turma.modalidade, status=Inscricao.STATUS_CONFIRMADO).count()

    if inscritos_atuais >= turma.capacidade:
        return Response({"detail": "A turma já atingiu a capacidade máxima."}, status=status.HTTP_400_BAD_REQUEST)

    if aluno.modalidades_inscritas.filter(pk=turma.modalidade_id).exists():
        return Response({"detail": "O aluno já está inscrito nessa turma."}, status=status.HTTP_400_BAD_REQUEST)

    if aluno.plano and aluno.modalidades_inscritas.count() >= aluno.plano.modalidades_inclusas:
        return Response({"detail": "O plano do aluno não permite mais modalidades."}, status=status.HTTP_400_BAD_REQUEST)

    inscricao = Inscricao.objects.create(
        aluno=aluno,
        modalidade=turma.modalidade,
        data=timezone.localdate(),
        hora=timezone.localtime().time().replace(microsecond=0),
    )
    inscricao.confirmar()
    return Response(InscricaoSerializer(inscricao).data, status=status.HTTP_201_CREATED)


@extend_schema(
    methods=["DELETE"],
    summary="Cancela a inscrição de um aluno na turma",
    responses={200: InscricaoSerializer},
    tags=["Turmas"],
)
@api_view(["DELETE"])
@permission_classes([IsAuthenticated, IsAdminOrFuncionarioProfile])
def cancelar_inscricao_turma_api(request, pk):
    inscricao = get_object_or_404(Inscricao, pk=pk, status=Inscricao.STATUS_CONFIRMADO)
    inscricao.cancelar()
    return Response(InscricaoSerializer(inscricao).data)


@perfil_required(Usuario.PERFIL_ALUNO)
@require_POST
def criar_inscricao_view(request):
    data = get_json_data(request)
    serializer = InscricaoSerializer(data=data)
    if serializer.is_valid():
        aluno = get_aluno_from_user(request.user)
        modalidade = serializer.validated_data["modalidade"]
        if not aluno or serializer.validated_data["aluno"] != aluno:
            return JsonResponse({"detail": "Aluno inválido para o usuário logado."}, status=403)
        if not aluno.plano:
            return JsonResponse({"detail": "Você precisa estar vinculado a um plano."}, status=400)
        if aluno.modalidades_inscritas.filter(pk=modalidade.pk).exists():
            return JsonResponse({"detail": "Você já está registrado nessa modalidade."}, status=400)
        if aluno.modalidades_inscritas.count() >= aluno.plano.modalidades_inclusas:
            return JsonResponse({"detail": "Seu plano não permite registrar mais modalidades."}, status=400)
        inscricao = serializer.save(status=Inscricao.STATUS_CONFIRMADO)
        inscricao.confirmar()
        return JsonResponse(InscricaoSerializer(inscricao).data, status=201)
    return JsonResponse(serializer.errors, status=400)


@perfil_required(Usuario.PERFIL_ALUNO)
@require_POST
def cancelar_inscricao_view(request, pk):
    aluno = get_aluno_from_user(request.user)
    inscricao = get_object_or_404(Inscricao, pk=pk, aluno=aluno, status=Inscricao.STATUS_CONFIRMADO)
    inscricao.cancelar()
    return JsonResponse(InscricaoSerializer(inscricao).data)


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

    inscricao = Inscricao.objects.create(
        aluno=aluno,
        modalidade=modalidade,
        data=timezone.localdate(),
        hora=timezone.now().time().replace(microsecond=0),
    )
    inscricao.confirmar()
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

    inscricao = get_confirmed_inscricao(aluno, modalidade)
    if inscricao:
        inscricao.cancelar()
    messages.success(request, "Registro cancelado com sucesso.")
    return redirect("listar_modalidades")


@login_required(login_url="login")
@require_http_methods(["GET", "POST"])
def listar_frequencias(request):
    if request.method == "POST":
        serializer = FrequenciaSerializer(data=get_json_data(request))
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

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
@require_http_methods(["GET", "POST", "PUT", "PATCH", "DELETE"])
def editar_frequencia(request, pk):
    frequencia = get_object_or_404(Frequencia, pk=pk)
    if request.method == "DELETE":
        frequencia.delete()
        return HttpResponse(status=204)
    if request.method in {"PUT", "PATCH"}:
        serializer = FrequenciaSerializer(frequencia, data=get_json_data(request), partial=request.method == "PATCH")
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)
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
@require_http_methods(["POST", "DELETE"])
def excluir_frequencia(request, pk):
    frequencia = get_object_or_404(Frequencia, pk=pk)
    frequencia.delete()
    if request.method == "DELETE":
        return HttpResponse(status=204)
    return redirect("listar_frequencias")


@extend_schema(
    methods=["POST"],
    summary="Confirma uma inscrição",
    responses={200: InscricaoSerializer},
    tags=["Inscrições"],
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def confirmar_inscricao_api(request, pk):
    inscricao = get_object_or_404(Inscricao, pk=pk)
    inscricao.confirmar()
    return Response(InscricaoSerializer(inscricao).data)
