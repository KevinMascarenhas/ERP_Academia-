from rest_framework import serializers

from .models import Plano


class PlanoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plano
        fields = [
            "id_plano",
            "nome_plano",
            "preco",
            "modalidades_inclusas",
            "duracao_meses",
        ]
