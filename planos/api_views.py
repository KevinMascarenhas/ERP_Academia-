from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Plano
from .serializers import PlanoSerializer


@extend_schema(tags=["Planos"])
class PlanoListCreateApiView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(summary="Listar planos", responses=PlanoSerializer(many=True))
    def get(self, request):
        planos = Plano.objects.all().order_by("id_plano")
        serializer = PlanoSerializer(planos, many=True)
        return Response(serializer.data)

    @extend_schema(summary="Criar plano", request=PlanoSerializer, responses={201: PlanoSerializer})
    def post(self, request):
        serializer = PlanoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@extend_schema(tags=["Planos"])
class PlanoDetailApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, id_plano):
        return Plano.objects.get(id_plano=id_plano)

    @extend_schema(summary="Detalhar plano", responses=PlanoSerializer)
    def get(self, request, id_plano):
        serializer = PlanoSerializer(self.get_object(id_plano))
        return Response(serializer.data)

    @extend_schema(summary="Atualizar plano", request=PlanoSerializer, responses=PlanoSerializer)
    def put(self, request, id_plano):
        plano = self.get_object(id_plano)
        serializer = PlanoSerializer(plano, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @extend_schema(summary="Atualizar parcialmente plano", request=PlanoSerializer, responses=PlanoSerializer)
    def patch(self, request, id_plano):
        plano = self.get_object(id_plano)
        serializer = PlanoSerializer(plano, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @extend_schema(summary="Excluir plano", responses={204: None})
    def delete(self, request, id_plano):
        plano = self.get_object(id_plano)
        plano.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
