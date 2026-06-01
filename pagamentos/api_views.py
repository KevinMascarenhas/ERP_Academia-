from drf_spectacular.utils import extend_schema
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Pagamento
from .serializers import PagamentoSerializer


@extend_schema(tags=["Pagamentos"])
class PagamentoListCreateApiView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(summary="Listar pagamentos", responses=PagamentoSerializer(many=True))
    def get(self, request):
        serializer = PagamentoSerializer(Pagamento.objects.all().order_by("-mes_ano"), many=True)
        return Response(serializer.data)

    @extend_schema(summary="Criar pagamento", request=PagamentoSerializer, responses={201: PagamentoSerializer})
    def post(self, request):
        serializer = PagamentoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@extend_schema(tags=["Pagamentos"])
class PagamentoDetailApiView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(summary="Detalhar pagamento", responses=PagamentoSerializer)
    def get(self, request, id):
        pagamento = get_object_or_404(Pagamento, id=id)
        return Response(PagamentoSerializer(pagamento).data)

    @extend_schema(summary="Atualizar pagamento", request=PagamentoSerializer, responses=PagamentoSerializer)
    def put(self, request, id):
        pagamento = get_object_or_404(Pagamento, id=id)
        serializer = PagamentoSerializer(pagamento, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @extend_schema(summary="Atualizar parcialmente pagamento", request=PagamentoSerializer, responses=PagamentoSerializer)
    def patch(self, request, id):
        pagamento = get_object_or_404(Pagamento, id=id)
        serializer = PagamentoSerializer(pagamento, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @extend_schema(summary="Excluir pagamento", responses={204: None})
    def delete(self, request, id):
        pagamento = get_object_or_404(Pagamento, id=id)
        pagamento.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
