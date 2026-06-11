from django.contrib import admin
from .models import Plano

@admin.register(Plano)
class PlanoAdmin(admin.ModelAdmin):
    list_display = ('nome_plano', 'preco', 'modalidades_inclusas', 'duracao_meses')
    search_fields = ('nome_plano',)
    ordering = ('nome_plano',)