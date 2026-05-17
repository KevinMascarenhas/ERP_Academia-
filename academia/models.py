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
    PERFIL_ADMIN = "Administrador"
    PERFIL_FUNCIONARIO = "Funcionário"
    PERFIL_ALUNO = "Aluno"

    PERFIL_CHOICES = [
        (PERFIL_ADMIN, "Administrador"),
        (PERFIL_FUNCIONARIO, "Funcionário"),
        (PERFIL_ALUNO, "Aluno"),
    ]

    nome = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    perfil = models.CharField(max_length=20, choices=PERFIL_CHOICES)

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

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

# ALUNO
# Espelha: domain/entities/models.py -> class Aluno(Usuario)

class Aluno(Usuario):
    cpf = models.CharField(max_length=14, unique=True)
    plano = models.ForeignKey(
        "planos.Plano",
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name="alunos"
    )
    modalidades_inscritas = models.ManyToManyField(
        "modalidades.Modalidade",
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


