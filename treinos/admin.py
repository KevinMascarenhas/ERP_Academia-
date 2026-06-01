from django.contrib import admin
from .models import Treino

@admin.register(Treino)
class TreinoAdmin(admin.ModelAdmin):
    list_display = ('aluno', 'grupo_muscular', 'nome_treino', 'data', 'series', 'repeticoes')
    search_fields = ('aluno__nome', 'aluno__cpf', 'grupo_muscular', 'nome_treino')
    list_filter = ('data', 'grupo_muscular')
    ordering = ('-data', 'aluno__nome')