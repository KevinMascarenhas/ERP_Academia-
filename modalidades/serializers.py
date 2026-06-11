from rest_framework import serializers

from .models import Frequencia, Inscricao, Modalidade, Turma


class ModalidadeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Modalidade
        fields = ["id", "modalidade_nome", "categoria", "horario", "dias_semana"]


class TurmaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Turma
        fields = ["id", "modalidade", "nome", "capacidade"]


class InscricaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inscricao
        fields = ["id", "aluno", "modalidade", "data", "hora", "status"]
        read_only_fields = ["id", "status"]


class FrequenciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Frequencia
        fields = ["id", "aluno", "modalidade", "data", "hora"]
