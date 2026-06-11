from django.db import models
from academia.models import Aluno

# TREINO
# Espelha: domain/entities/treino.py -> class Treino

class Treino(models.Model):
    id_treino = models.AutoField(primary_key=True)
    nome_treino = models.CharField(max_length=100)
    descricao = models.TextField()
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name="historico_treinos")
    grupo_muscular = models.CharField(max_length=100)
    exercicios = models.JSONField(default=list, help_text="Lista de exercícios")
    series = models.PositiveIntegerField()
    repeticoes = models.PositiveIntegerField()
    data = models.DateField()

    class Meta:
        verbose_name = "Treino"
        verbose_name_plural = "Treinos"
        ordering = ["-data"]

    def __str__(self):
        return f"{self.aluno.nome} — {self.grupo_muscular} em {self.data}"