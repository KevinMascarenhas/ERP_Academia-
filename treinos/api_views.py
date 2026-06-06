from drf_spectacular.utils import extend_schema
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from academia.permissions import IsAdminOrFuncionarioProfile
from .models import Treino
from .serializers import SugestaoTreinoSerializer, TreinoSerializer


@extend_schema(tags=["Treinos"])
class TreinoListCreateApiView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrFuncionarioProfile]

    @extend_schema(summary="Listar treinos", responses=TreinoSerializer(many=True))
    def get(self, request):
        serializer = TreinoSerializer(Treino.objects.all().order_by("-data"), many=True)
        return Response(serializer.data)

    @extend_schema(summary="Criar treino", request=TreinoSerializer, responses={201: TreinoSerializer})
    def post(self, request):
        serializer = TreinoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@extend_schema(tags=["Treinos"])
class TreinoDetailApiView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrFuncionarioProfile]

    @extend_schema(summary="Detalhar treino", responses=TreinoSerializer)
    def get(self, request, id_treino):
        treino = get_object_or_404(Treino, id_treino=id_treino)
        return Response(TreinoSerializer(treino).data)

    @extend_schema(summary="Atualizar treino", request=TreinoSerializer, responses=TreinoSerializer)
    def put(self, request, id_treino):
        treino = get_object_or_404(Treino, id_treino=id_treino)
        serializer = TreinoSerializer(treino, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @extend_schema(summary="Atualizar parcialmente treino", request=TreinoSerializer, responses=TreinoSerializer)
    def patch(self, request, id_treino):
        treino = get_object_or_404(Treino, id_treino=id_treino)
        serializer = TreinoSerializer(treino, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @extend_schema(summary="Excluir treino", responses={204: None})
    def delete(self, request, id_treino):
        treino = get_object_or_404(Treino, id_treino=id_treino)
        treino.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(tags=["Treinos"])
class SugestaoTreinoApiView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(summary="Sugerir exercicios por grupo muscular", responses=SugestaoTreinoSerializer)
    def get(self, request):
        grupo = request.query_params.get("grupo")
        if not grupo:
            return Response(
                {"detail": "Informe o parâmetro 'grupo' na query string."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        tabela = {
            "Peito": ["Supino reto", "Supino inclinado", "Crucifixo", "Crossover"],
            "Costas": ["Puxada frontal", "Remada curvada", "Remada unilateral", "Pulldown"],
            "Pernas": ["Agachamento", "Leg press", "Cadeira extensora", "Cadeira flexora"],
            "Ombro": ["Desenvolvimento com halteres", "Elevação lateral", "Elevação frontal", "Encolhimento"],
            "Bíceps": ["Rosca direta", "Rosca alternada", "Rosca concentrada", "Rosca martelo"],
            "Tríceps": ["Tríceps testa", "Tríceps pulley", "Tríceps francês", "Mergulho no banco"],
            "Abdômen": ["Abdominal crunch", "Prancha", "Abdominal oblíquo", "Elevação de pernas"],
        }

        exercicios = []
        for chave, lista_exercicios in tabela.items():
            if chave.lower() == grupo.lower():
                exercicios = lista_exercicios
                break

        if not exercicios:
            return Response(
                {"detail": f"Grupo muscular '{grupo}' não reconhecido."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = SugestaoTreinoSerializer({"grupo_muscular": grupo, "exercicios": exercicios})
        return Response(serializer.data)
