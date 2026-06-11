from django.db import models


class Modalidade(models.Model):
    modalidade_nome = models.CharField(max_length=100)
    categoria = models.CharField(max_length=100)
    horario = models.CharField(max_length=10, help_text="Formato HH:MM")
    dias_semana = models.JSONField(default=list, blank=True)

    class Meta:
        verbose_name = "Modalidade"
        verbose_name_plural = "Modalidades"

    def tem_horario_fixo(self):
        return len(self.dias_semana) > 0

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        Turma.objects.get_or_create(
            modalidade=self,
            defaults={"nome": f"Turma {self.modalidade_nome}"},
        )

    def __str__(self):
        return f"{self.modalidade_nome} ({self.categoria})"


class Turma(models.Model):
    modalidade = models.OneToOneField(
        "modalidades.Modalidade",
        on_delete=models.CASCADE,
        related_name="turma",
    )
    nome = models.CharField(max_length=120)
    capacidade = models.PositiveIntegerField(default=30)

    class Meta:
        verbose_name = "Turma"
        verbose_name_plural = "Turmas"
        ordering = ["modalidade__modalidade_nome"]

    def __str__(self):
        return f"{self.nome} - {self.modalidade.modalidade_nome}"


class Inscricao(models.Model):
    STATUS_PENDENTE = "pendente"
    STATUS_CONFIRMADO = "confirmado"
    STATUS_CANCELADO = "cancelado"

    STATUS_CHOICES = [
        (STATUS_PENDENTE, "Pendente"),
        (STATUS_CONFIRMADO, "Confirmado"),
        (STATUS_CANCELADO, "Cancelado"),
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
        if self.aluno_id and self.modalidade_id:
            self.aluno.modalidades_inscritas.add(self.modalidade)

    def cancelar(self):
        self.status = self.STATUS_CANCELADO
        self.save()
        if self.aluno_id and self.modalidade_id:
            inscricao_confirmada_existe = Inscricao.objects.filter(
                aluno=self.aluno,
                modalidade=self.modalidade,
                status=self.STATUS_CONFIRMADO,
            ).exclude(pk=self.pk).exists()
            if not inscricao_confirmada_existe:
                self.aluno.modalidades_inscritas.remove(self.modalidade)

    def __str__(self):
        return f"{self.aluno.nome} - {self.modalidade.modalidade_nome} em {self.data} as {self.hora}"


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
        return f"{self.aluno.nome} - {self.modalidade.modalidade_nome} em {self.data}"
