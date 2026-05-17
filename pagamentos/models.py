from django.db import models
from academia.models import Aluno

# PAGAMENTO
# Espelha: domain/entities/pagamento.py -> class Pagamento

class Pagamento(models.Model):
    STATUS_PENDENTE = "pendente"
    STATUS_PAGO = "pago"
    STATUS_ATRASADO = "atrasado"

    STATUS_CHOICES = [
        (STATUS_PENDENTE, "Pendente"),
        (STATUS_PAGO, "Pago"),
        (STATUS_ATRASADO, "Atrasado"),
    ]

    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name="pagamentos")
    valor = models.DecimalField(max_digits=8, decimal_places=2)
    mes_ano = models.CharField(max_length=7, help_text="Formato MM/AAAA")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=STATUS_PENDENTE)
    data_pagamento = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name = "Pagamento"
        verbose_name_plural = "Pagamentos"
        ordering = ["-mes_ano"]

    def pagar(self, data_pagamento=None):
        self.status = self.STATUS_PAGO
        self.data_pagamento = data_pagamento
        self.save()

    def marcar_atrasado(self):
        if self.status == self.STATUS_PENDENTE:
            self.status = self.STATUS_ATRASADO
            self.save()

    def __str__(self):
        return f"{self.aluno.nome} — {self.mes_ano} ({self.status})"
