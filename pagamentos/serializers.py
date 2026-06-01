from rest_framework import serializers

from .models import Pagamento


class PagamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pagamento
        fields = ["id", "aluno", "valor", "mes_ano", "status", "data_pagamento"]
