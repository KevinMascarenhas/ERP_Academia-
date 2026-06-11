from django.db import models

# PLANO
# Espelha: domain/entities/plano.py -> class Plano

class Plano(models.Model):
    id_plano = models.AutoField(primary_key=True)
    nome_plano = models.CharField(max_length=100, unique=True)
    preco = models.DecimalField(max_digits=8, decimal_places=2)
    modalidades_inclusas = models.PositiveIntegerField(help_text="Quantidade de modalidades permitidas")
    duracao_meses = models.PositiveIntegerField()

    class Meta:
        verbose_name = "Plano"
        verbose_name_plural = "Planos"

    def __str__(self):
        return f"{self.nome_plano} — R$ {self.preco:.2f}/mês"
