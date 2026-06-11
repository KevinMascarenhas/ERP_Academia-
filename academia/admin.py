from django.contrib import admin
from .models import Usuario, Administrador, Funcionario, Aluno

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'perfil', 'is_staff', 'is_active')
    search_fields = ('nome', 'email')
    list_filter = ('perfil', 'is_staff', 'is_active')
    ordering = ('nome',)

@admin.register(Administrador)
class AdministradorAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'is_active')
    search_fields = ('nome', 'email')
    ordering = ('nome',)

@admin.register(Funcionario)
class FuncionarioAdmin(admin.ModelAdmin):
    list_display = ('id_funcionario', 'nome', 'email', 'is_active')
    search_fields = ('id_funcionario', 'nome', 'email')
    ordering = ('nome',)

@admin.register(Aluno)
class AlunoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'cpf', 'plano', 'is_active')
    search_fields = ('nome', 'email', 'cpf')
    list_filter = ('plano', 'is_active')
    filter_horizontal = ('modalidades_inscritas',)
    ordering = ('nome',)
