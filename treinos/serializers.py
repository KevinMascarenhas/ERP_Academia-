from rest_framework import serializers

from .models import Treino


class TreinoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Treino
        fields = [
            "id_treino",
            "nome_treino",
            "descricao",
            "aluno",
            "grupo_muscular",
            "exercicios",
            "series",
            "repeticoes",
            "data",
        ]


class SugestaoTreinoSerializer(serializers.Serializer):
    grupo_muscular = serializers.CharField()
    exercicios = serializers.ListField(child=serializers.CharField())
