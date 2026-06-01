from django.contrib import admin
from django.utils import timezone
from .models import Pagamento

@admin.register(Pagamento)
class PagamentoAdmin(admin.ModelAdmin):
    list_display = ('aluno', 'valor', 'mes_ano', 'status', 'data_pagamento')
    search_fields = ('aluno__nome', 'aluno__cpf', 'mes_ano')
    list_filter = ('status', 'mes_ano')
    ordering = ('-mes_ano', 'aluno__nome')
    actions = ['marcar_como_pago', 'marcar_como_atrasado']

    @admin.action(description="Marcar pagamentos selecionados como PAGO")
    def marcar_como_pago(self, request, queryset):
        hoje = timezone.now().date()
        for pagamento in queryset:
            pagamento.pagar(data_pagamento=hoje)
        self.message_user(request, f"{queryset.count()} pagamento(s) marcado(s) como pago(s).")

    @admin.action(description="Marcar pagamentos selecionados como ATRASADO")
    def marcar_como_atrasado(self, request, queryset):
        for pagamento in queryset:
            pagamento.marcar_atrasado()
        self.message_user(request, f"{queryset.count()} pagamento(s) marcado(s) como atrasado(s).")
