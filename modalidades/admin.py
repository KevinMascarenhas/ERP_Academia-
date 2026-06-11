from django.contrib import admin
from .models import Modalidade, Turma, Inscricao, Frequencia

@admin.register(Modalidade)
class ModalidadeAdmin(admin.ModelAdmin):
    list_display = ('modalidade_nome', 'categoria', 'horario')
    search_fields = ('modalidade_nome', 'categoria')
    list_filter = ('categoria',)
    ordering = ('modalidade_nome',)

@admin.register(Turma)
class TurmaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'modalidade', 'capacidade')
    search_fields = ('nome', 'modalidade__modalidade_nome')
    list_filter = ('modalidade',)
    ordering = ('modalidade__modalidade_nome',)

@admin.register(Inscricao)
class InscricaoAdmin(admin.ModelAdmin):
    list_display = ('aluno', 'modalidade', 'data', 'hora', 'status')
    search_fields = ('aluno__nome', 'aluno__cpf', 'modalidade__modalidade_nome')
    list_filter = ('status', 'data', 'modalidade')
    ordering = ('-data', '-hora')
    actions = ['confirmar_inscricoes', 'cancelar_inscricoes']

    @admin.action(description="Confirmar inscrições selecionadas")
    def confirmar_inscricoes(self, request, queryset):
        for inscricao in queryset:
            inscricao.confirmar()
        self.message_user(request, f"{queryset.count()} inscrição(ões) confirmada(s) com sucesso.")

    @admin.action(description="Cancelar inscrições selecionadas")
    def cancelar_inscricoes(self, request, queryset):
        for inscricao in queryset:
            inscricao.cancelar()
        self.message_user(request, f"{queryset.count()} inscrição(ões) cancelada(s) com sucesso.")

@admin.register(Frequencia)
class FrequenciaAdmin(admin.ModelAdmin):
    list_display = ('aluno', 'modalidade', 'data', 'hora')
    search_fields = ('aluno__nome', 'aluno__cpf', 'modalidade__modalidade_nome')
    list_filter = ('data', 'modalidade')
    ordering = ('-data', '-hora')
