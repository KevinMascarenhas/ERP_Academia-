# academia/models.py — Django ORM
# Refatorado com herança de models, espelhando a estrutura do domain/

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# MANAGER

class UsuarioManager(BaseUserManager):
    def create_user(self, email, nome, perfil="Administrador", password=None, **extra):
        if not email:
            raise ValueError("Email é obrigatório.")
        email = self.normalize_email(email)
        user = self.model(email=email, nome=nome, perfil=perfil, **extra)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nome, password=None, **extra):
        extra.setdefault("perfil", "Administrador")
        extra.setdefault("is_staff", True)
        extra.setdefault("is_superuser", True)
        return self.create_user(email, nome, password=password, **extra)

# USUARIO (base para Administrador, Funcionario e Aluno)
# Espelha: domain/entities/models.py → class Usuario(ABC)

class Usuario(AbstractBaseUser):
    PERFIL_ADMIN       = "Administrador"
    PERFIL_FUNCIONARIO = "Funcionário"
    PERFIL_ALUNO       = "Aluno"

    PERFIL_CHOICES = [
        (PERFIL_ADMIN, "Administrador"),
        (PERFIL_FUNCIONARIO, "Funcionário"),
        (PERFIL_ALUNO, "Aluno"),
    ]

    nome = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    perfil = models.CharField(max_length=20, choices=PERFIL_CHOICES)

    is_staff     = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD  = "email"
    REQUIRED_FIELDS = ["nome"]

    objects = UsuarioManager()

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

    def get_perfil(self):
        return self.perfil

    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"

    def __str__(self):
        return f"{self.nome} ({self.perfil})"

# ADMINISTRADOR
# Espelha: domain/entities/models.py → class Administrador(Usuario)

class Administrador(Usuario):
    """
    Não tem campos extras — herda tudo de Usuario.
    O Django cria uma tabela 'academia_administrador' com apenas
    um FK para 'academia_usuario'.
    """

    class Meta:
        verbose_name = "Administrador"
        verbose_name_plural = "Administradores"

    def save(self, *args, **kwargs):
        self.perfil = self.PERFIL_ADMIN
        super().save(*args, **kwargs)

# FUNCIONARIO
# Espelha: domain/entities/funcionario.py → class Funcionario(Usuario)

class Funcionario(Usuario):
    id_funcionario = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = "Funcionário"
        verbose_name_plural = "Funcionários"

    def save(self, *args, **kwargs):
        self.perfil = self.PERFIL_FUNCIONARIO
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nome} | ID: {self.id_funcionario}"

# PLANO
# Espelha: domain/entities/plano.py → class Plano

class Plano(models.Model):
    nome_plano = models.CharField(max_length=100, unique=True)
    preco = models.DecimalField(max_digits=8, decimal_places=2)
    modalidades_inclusas = models.PositiveIntegerField(help_text="Quantidade de modalidades permitidas")
    duracao_meses = models.PositiveIntegerField()

    class Meta:
        verbose_name = "Plano"
        verbose_name_plural = "Planos"

    def __str__(self):
        return f"{self.nome_plano} — R$ {self.preco}/mês"

# MODALIDADE
# Espelha: domain/entities/modalidade.py → class Modalidade

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

# ALUNO
# Espelha: domain/entities/models.py → class Aluno(Usuario)

class Aluno(Usuario):
    cpf = models.CharField(max_length=14, unique=True)
    plano = models.ForeignKey(
        Plano,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name="alunos"
    )
    modalidades_inscritas = models.ManyToManyField(
        Modalidade,
        blank=True,
        related_name="alunos_inscritos"
    )

    class Meta:
        verbose_name = "Aluno"
        verbose_name_plural = "Alunos"

    def save(self, *args, **kwargs):
        self.perfil = self.PERFIL_ALUNO
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nome} | CPF: {self.cpf}"

# INSCRIÇÃO
# Espelha: domain/entities/inscricao.py → class Inscricao

class Inscricao(models.Model):
    STATUS_PENDENTE = "pendente"
    STATUS_CONFIRMADO = "confirmado"
    STATUS_CANCELADO = "cancelado"

    STATUS_CHOICES = [
        (STATUS_PENDENTE,   "Pendente"),
        (STATUS_CONFIRMADO, "Confirmado"),
        (STATUS_CANCELADO,  "Cancelado"),
    ]

    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name="agenda")
    modalidade = models.ForeignKey(Modalidade, on_delete=models.CASCADE)
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
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name="historico")
    modalidade = models.ForeignKey(Modalidade, on_delete=models.CASCADE)
    data = models.DateField(null=True, blank=True)
    hora = models.TimeField(null=True, blank=True)

    class Meta:
        verbose_name = "Frequência"
        verbose_name_plural = "Frequências"
        ordering = ["-data", "-hora"]

    def __str__(self):
        return f"{self.aluno.nome} — {self.modalidade.modalidade_nome} em {self.data}"



# TREINO
# Espelha: domain/entities/treino.py → class Treino


class Treino(models.Model):
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


# PAGAMENTO
# Espelha: domain/entities/pagamento.py → class Pagamento


class Pagamento(models.Model):
    STATUS_PENDENTE = "pendente"
    STATUS_PAGO     = "pago"
    STATUS_ATRASADO = "atrasado"

    STATUS_CHOICES = [
        (STATUS_PENDENTE, "Pendente"),
        (STATUS_PAGO,     "Pago"),
        (STATUS_ATRASADO, "Atrasado"),
    ]

    aluno          = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name="pagamentos")
    valor          = models.DecimalField(max_digits=8, decimal_places=2)
    mes_ano        = models.CharField(max_length=7, help_text="Formato MM/AAAA")
    status         = models.CharField(max_length=10, choices=STATUS_CHOICES, default=STATUS_PENDENTE)
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