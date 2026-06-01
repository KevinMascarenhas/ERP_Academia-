from django.test import TestCase
from django.utils import timezone
from academia.models import Aluno
from planos.models import Plano
from pagamentos.models import Pagamento

class PagamentosTestCase(TestCase):
    def setUp(self):
        self.plano = Plano.objects.create(
            nome_plano="Plano Pág",
            preco=120.00,
            modalidades_inclusas=2,
            duracao_meses=1
        )
        self.aluno = Aluno.objects.create(
            email="alunopag@academia.com",
            nome="Mariana Pag",
            cpf="555.666.777-88",
            plano=self.plano
        )

    def test_pagamento_creation_default_status(self):
        pagamento = Pagamento.objects.create(
            aluno=self.aluno,
            valor=120.00,
            mes_ano="05/2026"
        )
        self.assertEqual(pagamento.aluno, self.aluno)
        self.assertEqual(float(pagamento.valor), 120.00)
        self.assertEqual(pagamento.mes_ano, "05/2026")
        self.assertEqual(pagamento.status, Pagamento.STATUS_PENDENTE)
        self.assertIsNone(pagamento.data_pagamento)

    def test_pagar_method(self):
        pagamento = Pagamento.objects.create(
            aluno=self.aluno,
            valor=120.00,
            mes_ano="05/2026"
        )
        hoje = timezone.now().date()
        pagamento.pagar(data_pagamento=hoje)
        self.assertEqual(pagamento.status, Pagamento.STATUS_PAGO)
        self.assertEqual(pagamento.data_pagamento, hoje)

    def test_marcar_atrasado_method(self):
        pagamento = Pagamento.objects.create(
            aluno=self.aluno,
            valor=120.00,
            mes_ano="05/2026",
            status=Pagamento.STATUS_PENDENTE
        )
        pagamento.marcar_atrasado()
        self.assertEqual(pagamento.status, Pagamento.STATUS_ATRASADO)

        # Se já estiver pago, não deve mudar para atrasado
        pagamento_pago = Pagamento.objects.create(
            aluno=self.aluno,
            valor=120.00,
            mes_ano="06/2026",
            status=Pagamento.STATUS_PAGO
        )
        pagamento_pago.marcar_atrasado()
        self.assertEqual(pagamento_pago.status, Pagamento.STATUS_PAGO)
