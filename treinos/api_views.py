from drf_spectacular.utils import extend_schema
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Treino
from .serializers import TreinoSerializer


@extend_schema(tags=["Treinos"])
class TreinoListCreateApiView(APIView):
    permission_classes = [IsAuthenticated]

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
    permission_classes = [IsAuthenticated]

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
