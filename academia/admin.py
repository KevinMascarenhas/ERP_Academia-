from django.contrib import admin
from .models import Usuario, Administrador, Funcionario, Aluno
from planos.models import Plano
from modalidades.models import Modalidade, Inscricao, Frequencia
from treinos.models import Treino
from pagamentos.models import Pagamento

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