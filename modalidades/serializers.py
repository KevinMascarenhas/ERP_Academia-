from rest_framework import serializers

from .models import Frequencia, Inscricao, Modalidade


class ModalidadeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Modalidade
        fields = ["id", "modalidade_nome", "categoria", "horario", "dias_semana"]


class InscricaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inscricao
        fields = ["id", "aluno", "modalidade", "data", "hora", "status"]


class FrequenciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Frequencia
        fields = ["id", "aluno", "modalidade", "data", "hora"]
