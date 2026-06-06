from drf_spectacular.utils import extend_schema
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Administrador, Aluno, Funcionario, Usuario
from .permissions import IsAdminOrFuncionarioProfile, IsAdminProfile
from .serializers import (
    AdministradorSerializer,
    AlunoSerializer,
    FuncionarioSerializer,
    UsuarioSerializer,
)


@extend_schema(tags=["Academia"])
class UsuarioListCreateApiView(APIView):
    permission_classes = [IsAuthenticated, IsAdminProfile]

    @extend_schema(summary="Listar usuarios", responses=UsuarioSerializer(many=True))
    def get(self, request):
        serializer = UsuarioSerializer(Usuario.objects.all().order_by("id"), many=True)
        return Response(serializer.data)

    @extend_schema(summary="Criar usuario", request=UsuarioSerializer, responses={201: UsuarioSerializer})
    def post(self, request):
        serializer = UsuarioSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@extend_schema(tags=["Academia"])
class AdministradorListCreateApiView(APIView):
    permission_classes = [IsAuthenticated, IsAdminProfile]

    @extend_schema(summary="Listar administradores", responses=AdministradorSerializer(many=True))
    def get(self, request):
        serializer = AdministradorSerializer(Administrador.objects.all().order_by("id"), many=True)
        return Response(serializer.data)

    @extend_schema(summary="Criar administrador", request=AdministradorSerializer, responses={201: AdministradorSerializer})
    def post(self, request):
        serializer = AdministradorSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@extend_schema(tags=["Academia"])
class FuncionarioListCreateApiView(APIView):
    permission_classes = [IsAuthenticated, IsAdminProfile]
    
    @extend_schema(summary="Listar funcionarios", responses=FuncionarioSerializer(many=True))
    def get(self, request):
        serializer = FuncionarioSerializer(Funcionario.objects.all().order_by("id"), many=True)
        return Response(serializer.data)

    @extend_schema(summary="Criar funcionario", request=FuncionarioSerializer, responses={201: FuncionarioSerializer})
    def post(self, request):
        serializer = FuncionarioSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@extend_schema(tags=["Academia"])
class AlunoListCreateApiView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrFuncionarioProfile]

    @extend_schema(summary="Listar alunos", responses=AlunoSerializer(many=True))
    def get(self, request):
        serializer = AlunoSerializer(Aluno.objects.all().order_by("id"), many=True)
        return Response(serializer.data)

    @extend_schema(summary="Criar aluno", request=AlunoSerializer, responses={201: AlunoSerializer})
    def post(self, request):
        serializer = AlunoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@extend_schema(tags=["Academia"])
class UsuarioDetailApiView(APIView):
    permission_classes = [IsAuthenticated, IsAdminProfile]

    @extend_schema(summary="Detalhar usuario", responses=UsuarioSerializer)
    def get(self, request, id):
        return Response(UsuarioSerializer(get_object_or_404(Usuario, id=id)).data)

    @extend_schema(summary="Atualizar usuario", request=UsuarioSerializer, responses=UsuarioSerializer)
    def put(self, request, id):
        usuario = get_object_or_404(Usuario, id=id)
        serializer = UsuarioSerializer(usuario, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @extend_schema(summary="Atualizar parcialmente usuario", request=UsuarioSerializer, responses=UsuarioSerializer)
    def patch(self, request, id):
        usuario = get_object_or_404(Usuario, id=id)
        serializer = UsuarioSerializer(usuario, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @extend_schema(summary="Excluir usuario", responses={204: None})
    def delete(self, request, id):
        get_object_or_404(Usuario, id=id).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(tags=["Academia"])
class AdministradorDetailApiView(APIView):
    permission_classes = [IsAuthenticated, IsAdminProfile]

    @extend_schema(summary="Detalhar administrador", responses=AdministradorSerializer)
    def get(self, request, id):
        return Response(AdministradorSerializer(get_object_or_404(Administrador, id=id)).data)

    @extend_schema(summary="Atualizar administrador", request=AdministradorSerializer, responses=AdministradorSerializer)
    def put(self, request, id):
        administrador = get_object_or_404(Administrador, id=id)
        serializer = AdministradorSerializer(administrador, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @extend_schema(summary="Atualizar parcialmente administrador", request=AdministradorSerializer, responses=AdministradorSerializer)
    def patch(self, request, id):
        administrador = get_object_or_404(Administrador, id=id)
        serializer = AdministradorSerializer(administrador, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @extend_schema(summary="Excluir administrador", responses={204: None})
    def delete(self, request, id):
        get_object_or_404(Administrador, id=id).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(tags=["Academia"])
class FuncionarioDetailApiView(APIView):
    permission_classes = [IsAuthenticated, IsAdminProfile]

    @extend_schema(summary="Detalhar funcionario", responses=FuncionarioSerializer)
    def get(self, request, id):
        return Response(FuncionarioSerializer(get_object_or_404(Funcionario, id=id)).data)

    @extend_schema(summary="Atualizar funcionario", request=FuncionarioSerializer, responses=FuncionarioSerializer)
    def put(self, request, id):
        funcionario = get_object_or_404(Funcionario, id=id)
        serializer = FuncionarioSerializer(funcionario, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @extend_schema(summary="Atualizar parcialmente funcionario", request=FuncionarioSerializer, responses=FuncionarioSerializer)
    def patch(self, request, id):
        funcionario = get_object_or_404(Funcionario, id=id)
        serializer = FuncionarioSerializer(funcionario, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @extend_schema(summary="Excluir funcionario", responses={204: None})
    def delete(self, request, id):
        get_object_or_404(Funcionario, id=id).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(tags=["Academia"])
class AlunoDetailApiView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrFuncionarioProfile]

    @extend_schema(summary="Detalhar aluno", responses=AlunoSerializer)
    def get(self, request, id):
        return Response(AlunoSerializer(get_object_or_404(Aluno, id=id)).data)

    @extend_schema(summary="Atualizar aluno", request=AlunoSerializer, responses=AlunoSerializer)
    def put(self, request, id):
        aluno = get_object_or_404(Aluno, id=id)
        serializer = AlunoSerializer(aluno, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @extend_schema(summary="Atualizar parcialmente aluno", request=AlunoSerializer, responses=AlunoSerializer)
    def patch(self, request, id):
        aluno = get_object_or_404(Aluno, id=id)
        serializer = AlunoSerializer(aluno, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @extend_schema(summary="Excluir aluno", responses={204: None})
    def delete(self, request, id):
        get_object_or_404(Aluno, id=id).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
