from django.contrib import admin
from .models import Usuario, Administrador, Funcionario, Aluno, Plano, Modalidade, Inscricao, Frequencia, Treino, Pagamento

admin.site.register(Usuario)
admin.site.register(Administrador)
admin.site.register(Funcionario)
admin.site.register(Aluno)
admin.site.register(Plano)
admin.site.register(Modalidade)
admin.site.register(Inscricao)
admin.site.register(Frequencia)
admin.site.register(Treino)
admin.site.register(Pagamento)