from drf_spectacular.utils import extend_schema
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Frequencia, Inscricao, Modalidade
from .serializers import FrequenciaSerializer, InscricaoSerializer, ModalidadeSerializer


@extend_schema(tags=["Modalidades"])
class ModalidadeListCreateApiView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(summary="Listar modalidades", responses=ModalidadeSerializer(many=True))
    def get(self, request):
        serializer = ModalidadeSerializer(Modalidade.objects.all().order_by("id"), many=True)
        return Response(serializer.data)

    @extend_schema(summary="Criar modalidade", request=ModalidadeSerializer, responses={201: ModalidadeSerializer})
    def post(self, request):
        serializer = ModalidadeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@extend_schema(tags=["Modalidades"])
class InscricaoListCreateApiView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(summary="Listar inscricoes", responses=InscricaoSerializer(many=True))
    def get(self, request):
        serializer = InscricaoSerializer(Inscricao.objects.all().order_by("id"), many=True)
        return Response(serializer.data)

    @extend_schema(summary="Criar inscricao", request=InscricaoSerializer, responses={201: InscricaoSerializer})
    def post(self, request):
        serializer = InscricaoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@extend_schema(tags=["Modalidades"])
class FrequenciaListCreateApiView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(summary="Listar frequencias", responses=FrequenciaSerializer(many=True))
    def get(self, request):
        serializer = FrequenciaSerializer(Frequencia.objects.all().order_by("-data", "-hora"), many=True)
        return Response(serializer.data)

    @extend_schema(summary="Criar frequencia", request=FrequenciaSerializer, responses={201: FrequenciaSerializer})
    def post(self, request):
        serializer = FrequenciaSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@extend_schema(tags=["Modalidades"])
class ModalidadeDetailApiView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(summary="Detalhar modalidade", responses=ModalidadeSerializer)
    def get(self, request, id):
        return Response(ModalidadeSerializer(get_object_or_404(Modalidade, id=id)).data)

    @extend_schema(summary="Atualizar modalidade", request=ModalidadeSerializer, responses=ModalidadeSerializer)
    def put(self, request, id):
        modalidade = get_object_or_404(Modalidade, id=id)
        serializer = ModalidadeSerializer(modalidade, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @extend_schema(summary="Atualizar parcialmente modalidade", request=ModalidadeSerializer, responses=ModalidadeSerializer)
    def patch(self, request, id):
        modalidade = get_object_or_404(Modalidade, id=id)
        serializer = ModalidadeSerializer(modalidade, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @extend_schema(summary="Excluir modalidade", responses={204: None})
    def delete(self, request, id):
        get_object_or_404(Modalidade, id=id).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(tags=["Modalidades"])
class InscricaoDetailApiView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(summary="Detalhar inscricao", responses=InscricaoSerializer)
    def get(self, request, id):
        return Response(InscricaoSerializer(get_object_or_404(Inscricao, id=id)).data)

    @extend_schema(summary="Atualizar inscricao", request=InscricaoSerializer, responses=InscricaoSerializer)
    def put(self, request, id):
        inscricao = get_object_or_404(Inscricao, id=id)
        serializer = InscricaoSerializer(inscricao, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @extend_schema(summary="Atualizar parcialmente inscricao", request=InscricaoSerializer, responses=InscricaoSerializer)
    def patch(self, request, id):
        inscricao = get_object_or_404(Inscricao, id=id)
        serializer = InscricaoSerializer(inscricao, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @extend_schema(summary="Excluir inscricao", responses={204: None})
    def delete(self, request, id):
        get_object_or_404(Inscricao, id=id).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(tags=["Modalidades"])
class FrequenciaDetailApiView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(summary="Detalhar frequencia", responses=FrequenciaSerializer)
    def get(self, request, id):
        return Response(FrequenciaSerializer(get_object_or_404(Frequencia, id=id)).data)

    @extend_schema(summary="Atualizar frequencia", request=FrequenciaSerializer, responses=FrequenciaSerializer)
    def put(self, request, id):
        frequencia = get_object_or_404(Frequencia, id=id)
        serializer = FrequenciaSerializer(frequencia, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @extend_schema(summary="Atualizar parcialmente frequencia", request=FrequenciaSerializer, responses=FrequenciaSerializer)
    def patch(self, request, id):
        frequencia = get_object_or_404(Frequencia, id=id)
        serializer = FrequenciaSerializer(frequencia, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @extend_schema(summary="Excluir frequencia", responses={204: None})
    def delete(self, request, id):
        get_object_or_404(Frequencia, id=id).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
