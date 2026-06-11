from functools import wraps
import json

from django.conf import settings as django_settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods, require_POST
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from modalidades.models import Frequencia, Modalidade
from pagamentos.models import Pagamento
from planos.models import Plano
from treinos.models import Treino

from .models import Administrador, Aluno, Funcionario, Usuario
from .permissions import IsAdminOrFuncionarioProfile, IsAdminProfile
from .serializers import AdministradorSerializer, AlunoSerializer, FuncionarioSerializer, UsuarioSerializer


def get_json_data(request):
    if not request.body:
        return {}
    try:
        return json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        return {}


def perfil_required(*perfis):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect("login")
            if request.user.perfil not in perfis:
                return render(request, "acesso_negado.html", {"usuario": request.user})
            return view_func(request, *args, **kwargs)

        return wrapper

    return decorator


def get_usuario_instance(user):
    for model in (Administrador, Funcionario, Aluno):
        instance = model.objects.filter(pk=user.pk).first()
        if instance:
            return instance
    return user


def get_aluno_from_user(user):
    return Aluno.objects.filter(pk=user.pk).select_related("plano").prefetch_related("modalidades_inscritas").first()


def can_manage_user(current_user, target_user):
    if current_user.perfil == Usuario.PERFIL_ADMIN:
        return True
    if current_user.perfil == Usuario.PERFIL_FUNCIONARIO and isinstance(target_user, Aluno):
        return True
    return False


def build_role_flags(user):
    return {
        "is_admin": user.perfil == Usuario.PERFIL_ADMIN,
        "is_funcionario": user.perfil == Usuario.PERFIL_FUNCIONARIO,
        "is_aluno": user.perfil == Usuario.PERFIL_ALUNO,
    }


def serialize_usuario_instance(usuario):
    if isinstance(usuario, Administrador):
        return AdministradorSerializer(usuario).data
    if isinstance(usuario, Funcionario):
        return FuncionarioSerializer(usuario).data
    if isinstance(usuario, Aluno):
        return AlunoSerializer(usuario).data
    return UsuarioSerializer(usuario).data


@extend_schema(
    methods=["GET"],
    summary="Lista todos os alunos",
    responses={200: AlunoSerializer(many=True)},
    tags=["Alunos"],
)
@extend_schema(
    methods=["POST"],
    summary="Cria um novo aluno",
    request=AlunoSerializer,
    responses={201: AlunoSerializer},
    tags=["Alunos"],
)
@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated, IsAdminOrFuncionarioProfile])
def alunos_api(request):
    if request.method == "GET":
        return Response(AlunoSerializer(Aluno.objects.select_related("plano").all(), many=True).data)
    serializer = AlunoSerializer(data=request.data)
    if serializer.is_valid():
        aluno = serializer.save()
        return Response(AlunoSerializer(aluno).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    methods=["GET"],
    summary="Lista todos os funcionários",
    responses={200: FuncionarioSerializer(many=True)},
    tags=["Funcionários"],
)
@extend_schema(
    methods=["POST"],
    summary="Cria um novo funcionário",
    request=FuncionarioSerializer,
    responses={201: FuncionarioSerializer},
    tags=["Funcionários"],
)
@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated, IsAdminProfile])
def funcionarios_api(request):
    if request.method == "GET":
        return Response(FuncionarioSerializer(Funcionario.objects.all(), many=True).data)
    serializer = FuncionarioSerializer(data=request.data)
    if serializer.is_valid():
        funcionario = serializer.save()
        return Response(FuncionarioSerializer(funcionario).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    methods=["GET"],
    summary="Lista todos os administradores",
    responses={200: AdministradorSerializer(many=True)},
    tags=["Administradores"],
)
@extend_schema(
    methods=["POST"],
    summary="Cria um novo administrador",
    request=AdministradorSerializer,
    responses={201: AdministradorSerializer},
    tags=["Administradores"],
)
@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated, IsAdminProfile])
def administradores_api(request):
    if request.method == "GET":
        return Response(AdministradorSerializer(Administrador.objects.all(), many=True).data)
    serializer = AdministradorSerializer(data=request.data)
    if serializer.is_valid():
        administrador = serializer.save()
        return Response(AdministradorSerializer(administrador).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    methods=["GET"],
    summary="Retorna detalhes de um usuário",
    responses={200: UsuarioSerializer},
    tags=["Usuários"],
)
@extend_schema(
    methods=["PUT"],
    summary="Atualiza um usuário (completo)",
    request=UsuarioSerializer,
    responses={200: UsuarioSerializer},
    tags=["Usuários"],
)
@extend_schema(
    methods=["PATCH"],
    summary="Atualiza um usuário (parcial)",
    request=UsuarioSerializer,
    responses={200: UsuarioSerializer},
    tags=["Usuários"],
)
@extend_schema(
    methods=["DELETE"],
    summary="Remove um usuário",
    responses={204: None},
    tags=["Usuários"],
)
@api_view(["GET", "PUT", "PATCH", "DELETE"])
@permission_classes([IsAuthenticated, IsAdminOrFuncionarioProfile])
def usuario_detail_api(request, user_id):
    usuario_base = get_object_or_404(Usuario, pk=user_id)
    usuario = get_usuario_instance(usuario_base)
    if not can_manage_user(request.user, usuario):
        return Response({"detail": "Acesso negado."}, status=status.HTTP_403_FORBIDDEN)

    if request.method == "GET":
        return Response(serialize_usuario_instance(usuario))

    if request.method == "DELETE":
        usuario.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    if isinstance(usuario, Administrador):
        serializer_class = AdministradorSerializer
    elif isinstance(usuario, Funcionario):
        serializer_class = FuncionarioSerializer
    elif isinstance(usuario, Aluno):
        serializer_class = AlunoSerializer
    else:
        serializer_class = UsuarioSerializer

    serializer = serializer_class(usuario, data=request.data, partial=request.method == "PATCH")
    if serializer.is_valid():
        usuario = serializer.save()
        return Response(serializer_class(usuario).data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def _set_jwt_cookies(response, user, secure=False):
    """Gera tokens JWT para o user e os define como cookies HttpOnly na response."""
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)
    refresh_token = str(refresh)

    access_lifetime = django_settings.SIMPLE_JWT.get("ACCESS_TOKEN_LIFETIME")
    refresh_lifetime = django_settings.SIMPLE_JWT.get("REFRESH_TOKEN_LIFETIME")

    response.set_cookie(
        "access_token",
        access_token,
        max_age=int(access_lifetime.total_seconds()),
        httponly=True,
        samesite="Lax",
        secure=secure,
    )
    response.set_cookie(
        "refresh_token",
        refresh_token,
        max_age=int(refresh_lifetime.total_seconds()),
        httponly=True,
        samesite="Lax",
        secure=secure,
    )
    return response


def login_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        email = request.POST.get("email", "").strip()
        senha = request.POST.get("password", "")
        user = authenticate(request, username=email, password=senha)

        if user is not None:
            login(request, user)
            response = redirect("dashboard")
            _set_jwt_cookies(response, user, secure=request.is_secure())
            return response

        return render(
            request,
            "login.html",
            {"erro": "E-mail ou senha inválidos.", "email": email},
        )

    return render(request, "login.html")


@login_required(login_url="login")
def logout_view(request):
    logout(request)
    response = redirect("login")
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return response


@login_required(login_url="login")
def dashboard_view(request):
    perfil = request.user.perfil
    if perfil == Usuario.PERFIL_ADMIN:
        return redirect("dashboard_admin")
    if perfil == Usuario.PERFIL_FUNCIONARIO:
        return redirect("dashboard_funcionario")
    if perfil == Usuario.PERFIL_ALUNO:
        return redirect("dashboard_aluno")
    return redirect("login")


def acesso_negado_view(request):
    return render(request, "acesso_negado.html", {"usuario": request.user})


@perfil_required(Usuario.PERFIL_ADMIN)
def dashboard_admin_view(request):
    context = {
        "usuario": request.user,
        "total_usuarios": Usuario.objects.count(),
        "total_administradores": Administrador.objects.count(),
        "total_funcionarios": Funcionario.objects.count(),
        "total_alunos": Aluno.objects.count(),
        "total_planos": Plano.objects.count(),
        "total_modalidades": Modalidade.objects.count(),
        "total_treinos": Treino.objects.count(),
        "total_pagamentos_pendentes": Pagamento.objects.filter(status=Pagamento.STATUS_PENDENTE).count(),
        **build_role_flags(request.user),
    }
    return render(request, "dashboard_admin.html", context)


@perfil_required(Usuario.PERFIL_FUNCIONARIO)
def dashboard_funcionario_view(request):
    context = {
        "usuario": request.user,
        "total_alunos": Aluno.objects.count(),
        "total_planos": Plano.objects.count(),
        "total_modalidades": Modalidade.objects.count(),
        "total_treinos": Treino.objects.count(),
        "total_frequencias": Frequencia.objects.count(),
        "pagamentos_pendentes": Pagamento.objects.filter(status=Pagamento.STATUS_PENDENTE).count(),
        **build_role_flags(request.user),
    }
    return render(request, "dashboard_funcionario.html", context)


@perfil_required(Usuario.PERFIL_ALUNO)
def dashboard_aluno_view(request):
    aluno = get_aluno_from_user(request.user)
    context = {
        "usuario": request.user,
        "aluno": aluno,
        "modalidades_registradas": aluno.modalidades_inscritas.all() if aluno else [],
        "treinos_recentes": Treino.objects.filter(aluno=aluno).order_by("-data")[:5] if aluno else [],
        "frequencias_recentes": Frequencia.objects.filter(aluno=aluno).order_by("-data", "-hora")[:5] if aluno else [],
        "total_frequencias": Frequencia.objects.filter(aluno=aluno).count() if aluno else 0,
        **build_role_flags(request.user),
    }
    return render(request, "dashboard_aluno.html", context)


@perfil_required(Usuario.PERFIL_ADMIN, Usuario.PERFIL_FUNCIONARIO)
def listar_usuarios(request):
    context = {
        "usuario": request.user,
        "administradores": Administrador.objects.order_by("nome") if request.user.perfil == Usuario.PERFIL_ADMIN else [],
        "funcionarios": Funcionario.objects.order_by("nome") if request.user.perfil == Usuario.PERFIL_ADMIN else [],
        "alunos": Aluno.objects.select_related("plano").order_by("nome"),
        **build_role_flags(request.user),
    }
    return render(request, "academia/listar_usuarios.html", context)


@perfil_required(Usuario.PERFIL_ADMIN, Usuario.PERFIL_FUNCIONARIO)
@require_http_methods(["GET", "POST"])
def criar_usuario_view(request):
    planos = Plano.objects.order_by("nome_plano")
    perfis_disponiveis = [Usuario.PERFIL_ALUNO]
    if request.user.perfil == Usuario.PERFIL_ADMIN:
        perfis_disponiveis = [Usuario.PERFIL_ALUNO, Usuario.PERFIL_FUNCIONARIO, Usuario.PERFIL_ADMIN]

    if request.method == "POST":
        perfil = request.POST.get("perfil") or Usuario.PERFIL_ALUNO
        if perfil not in perfis_disponiveis:
            messages.error(request, "Você não pode criar esse tipo de usuário.")
            return redirect("criar_usuario")

        nome = request.POST.get("nome", "").strip()
        email = request.POST.get("email", "").strip().lower()
        password = request.POST.get("password", "")

        if not nome or not email or not password:
            messages.error(request, "Nome, e-mail e senha são obrigatórios.")
            return redirect("criar_usuario")

        if Usuario.objects.filter(email=email).exists():
            messages.error(request, "Já existe um usuário com esse e-mail.")
            return redirect("criar_usuario")

        if perfil == Usuario.PERFIL_ADMIN:
            usuario = Administrador(nome=nome, email=email, is_staff=True, is_superuser=True)
        elif perfil == Usuario.PERFIL_FUNCIONARIO:
            id_funcionario = request.POST.get("id_funcionario", "").strip()
            if not id_funcionario:
                messages.error(request, "Informe o ID do funcionário.")
                return redirect("criar_usuario")
            usuario = Funcionario(nome=nome, email=email, id_funcionario=id_funcionario)
        else:
            cpf = request.POST.get("cpf", "").strip()
            if not cpf:
                messages.error(request, "Informe o CPF do aluno.")
                return redirect("criar_usuario")
            plano_id = request.POST.get("plano")
            plano = Plano.objects.filter(id_plano=plano_id).first() if plano_id else None
            usuario = Aluno(nome=nome, email=email, cpf=cpf, plano=plano)

        usuario.set_password(password)
        usuario.save()
        messages.success(request, "Usuário criado com sucesso.")
        return redirect("listar_usuarios")

    context = {
        "usuario": request.user,
        "planos": planos,
        "perfis_disponiveis": perfis_disponiveis,
        **build_role_flags(request.user),
    }
    return render(request, "academia/criar_usuario.html", context)


@perfil_required(Usuario.PERFIL_ADMIN, Usuario.PERFIL_FUNCIONARIO)
@require_http_methods(["GET", "POST"])
def editar_usuario_view(request, user_id):
    usuario_base = get_object_or_404(Usuario, pk=user_id)
    usuario = get_usuario_instance(usuario_base)
    if not can_manage_user(request.user, usuario):
        return render(request, "acesso_negado.html", {"usuario": request.user})

    if request.method == "POST":
        usuario.nome = request.POST.get("nome", usuario.nome).strip()
        email = request.POST.get("email", usuario.email).strip().lower()
        if Usuario.objects.exclude(pk=usuario.pk).filter(email=email).exists():
            messages.error(request, "Já existe um usuário com esse e-mail.")
            return redirect("editar_usuario", user_id=user_id)
        usuario.email = email
        usuario.is_active = request.POST.get("is_active") == "on"

        nova_senha = request.POST.get("password", "").strip()
        if nova_senha:
            usuario.set_password(nova_senha)

        if isinstance(usuario, Funcionario):
            usuario.id_funcionario = request.POST.get("id_funcionario", usuario.id_funcionario).strip()

        if isinstance(usuario, Aluno):
            usuario.cpf = request.POST.get("cpf", usuario.cpf).strip()
            plano_id = request.POST.get("plano")
            usuario.plano = Plano.objects.filter(id_plano=plano_id).first() if plano_id else None

        usuario.save()
        messages.success(request, "Usuário atualizado com sucesso.")
        return redirect("listar_usuarios")

    context = {
        "usuario_logado": request.user,
        "usuario_editado": usuario,
        "planos": Plano.objects.order_by("nome_plano"),
        "tipo_usuario": usuario.__class__.__name__,
        **build_role_flags(request.user),
    }
    return render(request, "academia/editar_usuario.html", context)


@perfil_required(Usuario.PERFIL_ADMIN, Usuario.PERFIL_FUNCIONARIO)
@require_POST
def excluir_usuario_view(request, user_id):
    usuario_base = get_object_or_404(Usuario, pk=user_id)
    usuario = get_usuario_instance(usuario_base)
    if not can_manage_user(request.user, usuario):
        return render(request, "acesso_negado.html", {"usuario": request.user})

    usuario.delete()
    messages.success(request, "Usuário removido com sucesso.")
    return redirect("listar_usuarios")
