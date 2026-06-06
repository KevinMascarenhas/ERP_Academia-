from django.test import TestCase
from django.utils import timezone
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from academia.models import Aluno
from planos.models import Plano
from modalidades.models import Modalidade, Inscricao, Frequencia

class ModalidadesTestCase(TestCase):
    def setUp(self):
        self.plano = Plano.objects.create(
            nome_plano="Básico",
            preco=80.00,
            modalidades_inclusas=1,
            duracao_meses=1
        )
        self.aluno = Aluno.objects.create(
            email="aluno_teste@academia.com",
            nome="Joao Silva",
            cpf="987.654.321-11",
            plano=self.plano
        )
        self.modalidade_crossfit = Modalidade.objects.create(
            modalidade_nome="Crossfit",
            categoria="Funcional",
            horario="18:00",
            dias_semana=["Segunda", "Quarta", "Sexta"]
        )
        self.modalidade_musculacao = Modalidade.objects.create(
            modalidade_nome="Musculação",
            categoria="Força",
            horario="06:00",
            dias_semana=[]
        )

    def test_tem_horario_fixo(self):
        self.assertTrue(self.modalidade_crossfit.tem_horario_fixo())
        self.assertFalse(self.modalidade_musculacao.tem_horario_fixo())

    def test_inscricao_confirmar_e_cancelar(self):
        hoje = timezone.now().date()
        agora = timezone.now().time()
        inscricao = Inscricao.objects.create(
            aluno=self.aluno,
            modalidade=self.modalidade_crossfit,
            data=hoje,
            hora=agora,
            status=Inscricao.STATUS_PENDENTE
        )
        self.assertEqual(inscricao.status, Inscricao.STATUS_PENDENTE)

        # Confirmar
        inscricao.confirmar()
        self.assertEqual(inscricao.status, Inscricao.STATUS_CONFIRMADO)

        # Cancelar
        inscricao.cancelar()
        self.assertEqual(inscricao.status, Inscricao.STATUS_CANCELADO)

    def test_frequencia_creation(self):
        hoje = timezone.now().date()
        agora = timezone.now().time()
        frequencia = Frequencia.objects.create(
            aluno=self.aluno,
            modalidade=self.modalidade_musculacao,
            data=hoje,
            hora=agora
        )
        self.assertEqual(frequencia.aluno, self.aluno)
        self.assertEqual(frequencia.modalidade, self.modalidade_musculacao)
        self.assertEqual(frequencia.data, hoje)
        self.assertEqual(frequencia.hora, agora)


class ModalidadesApiTestCase(TestCase):
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
            nome_plano="API Plano",
            preco=90.00,
            modalidades_inclusas=2,
            duracao_meses=6,
        )
        self.aluno = Aluno.objects.create(
            email="alunoapi@academia.com",
            nome="Aluno API",
            cpf="999.888.777-66",
            plano=self.plano,
        )
        self.modalidade = Modalidade.objects.create(
            modalidade_nome="Funcional",
            categoria="Condicionamento",
            horario="18:00",
            dias_semana=["Segunda", "Quarta"],
        )
        self.inscricao = Inscricao.objects.create(
            aluno=self.aluno,
            modalidade=self.modalidade,
            data=timezone.localdate(),
            hora=timezone.now().time(),
        )

    def test_confirmar_inscricao(self):
        response = self.client.post(f"/api/modalidades/inscricoes/{self.inscricao.id}/confirmar/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.inscricao.refresh_from_db()
        self.assertEqual(self.inscricao.status, Inscricao.STATUS_CONFIRMADO)

    def test_cancelar_inscricao(self):
        response = self.client.post(f"/api/modalidades/inscricoes/{self.inscricao.id}/cancelar/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.inscricao.refresh_from_db()
        self.assertEqual(self.inscricao.status, Inscricao.STATUS_CANCELADO)
