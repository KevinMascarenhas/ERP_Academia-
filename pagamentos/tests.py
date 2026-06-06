from django.test import TestCase
from django.utils import timezone
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
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


class PagamentosApiTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        User = get_user_model()
        self.user = User.objects.create_user(
            email="api@academia.com",
            nome="API User",
            password="securepassword123",
        )
        self.client.force_authenticate(user=self.user)

        self.plano = Plano.objects.create(
            nome_plano="API Plano Pag",
            preco=120.00,
            modalidades_inclusas=2,
            duracao_meses=1,
        )
        self.aluno = Aluno.objects.create(
            email="alunopagapi@academia.com",
            nome="Mariana API",
            cpf="555.666.777-99",
            plano=self.plano,
        )
        self.pagamento = Pagamento.objects.create(
            aluno=self.aluno,
            valor=120.00,
            mes_ano="05/2026",
        )

    def test_marcar_pagamento_como_pago(self):
        response = self.client.post(f"/api/pagamentos/{self.pagamento.id}/pagar/", {"data_pagamento": "2026-06-02"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.pagamento.refresh_from_db()
        self.assertEqual(self.pagamento.status, Pagamento.STATUS_PAGO)
        self.assertEqual(str(self.pagamento.data_pagamento), "2026-06-02")

    def test_marcar_pagamento_como_atrasado(self):
        response = self.client.post(f"/api/pagamentos/{self.pagamento.id}/atrasar/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.pagamento.refresh_from_db()
        self.assertEqual(self.pagamento.status, Pagamento.STATUS_ATRASADO)
