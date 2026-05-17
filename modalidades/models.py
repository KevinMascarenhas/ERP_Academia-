from django.db import models
import academia

# MODALIDADE
# Espelha: domain/entities/modalidade.py -> class Modalidade

class Modalidade(models.Model):
    modalidade_nome = models.CharField(max_length=100)
    categoria = models.CharField(max_length=100)
    horario = models.CharField(max_length=10, help_text="Formato HH:MM")

    # Lista de dias ex: ["Terça", "Quinta"] ou [] para acesso livre (musculação)
    dias_semana = models.JSONField(default=list, blank=True)

    class Meta:
        verbose_name = "Modalidade"
        verbose_name_plural = "Modalidades"

    def tem_horario_fixo(self):
        return len(self.dias_semana) > 0

    def __str__(self):
        return f"{self.modalidade_nome} ({self.categoria})"
    
# INSCRIÇÃO
# Espelha: domain/entities/inscricao.py -> class Inscricao
    
class Inscricao(models.Model):
    STATUS_PENDENTE = "pendente"
    STATUS_CONFIRMADO = "confirmado"
    STATUS_CANCELADO = "cancelado"

    STATUS_CHOICES = [
        (STATUS_PENDENTE,   "Pendente"),
        (STATUS_CONFIRMADO, "Confirmado"),
        (STATUS_CANCELADO,  "Cancelado"),
    ]

    aluno = models.ForeignKey("academia.Aluno", on_delete=models.CASCADE, related_name="agenda")
    modalidade = models.ForeignKey("modalidades.Modalidade", on_delete=models.CASCADE)
    data = models.DateField()
    hora = models.TimeField()
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default=STATUS_PENDENTE)

    class Meta:
        verbose_name = "Inscrição"
        verbose_name_plural = "Inscrições"

    def confirmar(self):
        self.status = self.STATUS_CONFIRMADO
        self.save()

    def cancelar(self):
        self.status = self.STATUS_CANCELADO
        self.save()

    def __str__(self):
        return f"{self.aluno.nome} — {self.modalidade.modalidade_nome} em {self.data} às {self.hora}"


# FREQUÊNCIA
# Espelha: Aluno.frequentar() / Aluno.historico

class Frequencia(models.Model):
    aluno = models.ForeignKey("academia.Aluno", on_delete=models.CASCADE, related_name="historico")
    modalidade = models.ForeignKey("modalidades.Modalidade", on_delete=models.CASCADE)
    data = models.DateField(null=True, blank=True)
    hora = models.TimeField(null=True, blank=True)

    class Meta:
        verbose_name = "Frequência"
        verbose_name_plural = "Frequências"
        ordering = ["-data", "-hora"]

    def __str__(self):
        return f"{self.aluno.nome} — {self.modalidade.modalidade_nome} em {self.data}"

