from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from academia.models import Administrador, Aluno, Funcionario, Usuario
from modalidades.models import Modalidade
from planos.models import Plano
from treinos.models import Treino


class AcademiaModelsTestCase(TestCase):
    def setUp(self):
        self.plano_ouro = Plano.objects.create(
            nome_plano="Ouro",
            preco=150.00,
            modalidades_inclusas=3,
            duracao_meses=12,
        )

    def test_create_user(self):
        user = get_user_model().objects.create_user(
            email="test@user.com",
            nome="Test User",
            password="securepassword123",
        )
        self.assertEqual(user.email, "test@user.com")
        self.assertEqual(user.nome, "Test User")
        self.assertEqual(user.perfil, "Administrador")
        self.assertTrue(user.check_password("securepassword123"))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        admin_user = get_user_model().objects.create_superuser(
            email="admin@user.com",
            nome="Admin User",
            password="adminpassword123",
        )
        self.assertEqual(admin_user.email, "admin@user.com")
        self.assertEqual(admin_user.perfil, "Administrador")
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)

    def test_administrador_profile_auto_assignment(self):
        admin = Administrador.objects.create(email="adm@academia.com", nome="Carlos Admin")
        self.assertEqual(admin.perfil, Usuario.PERFIL_ADMIN)

    def test_funcionario_profile_auto_assignment(self):
        func = Funcionario.objects.create(
            email="func@academia.com",
            nome="Ana Func",
            id_funcionario="FUNC001",
        )
        self.assertEqual(func.perfil, Usuario.PERFIL_FUNCIONARIO)
        self.assertEqual(func.id_funcionario, "FUNC001")

    def test_aluno_profile_auto_assignment(self):
        aluno = Aluno.objects.create(
            email="aluno@academia.com",
            nome="Joao Aluno",
            cpf="123.456.789-00",
            plano=self.plano_ouro,
        )
        self.assertEqual(aluno.perfil, Usuario.PERFIL_ALUNO)
        self.assertEqual(aluno.cpf, "123.456.789-00")
        self.assertEqual(aluno.plano, self.plano_ouro)


class AcademiaApiPermissionsTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin = Administrador.objects.create(
            email="admin@academia.com",
            nome="Admin",
            is_staff=True,
            is_superuser=True,
        )
        self.admin.set_password("adminpass123")
        self.admin.save()

        self.funcionario = Funcionario.objects.create(
            email="func@academia.com",
            nome="Funcionario",
            id_funcionario="FUNC001",
        )
        self.funcionario.set_password("funcpass123")
        self.funcionario.save()

        self.usuario = get_user_model().objects.create_user(
            email="user@academia.com",
            nome="Usuario",
            password="userpass123",
        )

        self.aluno = Aluno.objects.create(
            email="aluno@academia.com",
            nome="Aluno",
            cpf="123.456.789-00",
        )
        self.aluno.set_password("alunopass123")
        self.aluno.save()

        self.plano = Plano.objects.create(
            nome_plano="Base",
            preco=100.00,
            modalidades_inclusas=1,
            duracao_meses=1,
        )

    def test_funcionario_agora_acessa_planos(self):
        self.client.force_authenticate(user=self.funcionario)
        response = self.client.get("/api/planos/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_acessa_planos(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.get("/api/planos/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_funcionario_acessa_alunos_na_api(self):
        self.client.force_authenticate(user=self.funcionario)
        response = self.client.get("/api/academia/alunos/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_funcionario_nao_acessa_funcionarios_na_api(self):
        self.client.force_authenticate(user=self.funcionario)
        response = self.client.get("/api/academia/funcionarios/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_usuario_hashes_password(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.patch(
            f"/api/academia/usuarios/{self.usuario.id}/",
            {"password": "newpass123"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.usuario.refresh_from_db()
        self.assertTrue(self.usuario.check_password("newpass123"))

    def test_update_usuario_accepts_blank_password_and_keeps_current_password(self):
        self.client.force_authenticate(user=self.admin)
        self.usuario.set_password("oldpass123")
        self.usuario.save()

        response = self.client.patch(
            f"/api/academia/usuarios/{self.usuario.id}/",
            {"nome": "Usuario Atualizado", "password": ""},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.usuario.refresh_from_db()
        self.assertEqual(self.usuario.nome, "Usuario Atualizado")
        self.assertTrue(self.usuario.check_password("oldpass123"))


class AcademiaWebProfilesTestCase(TestCase):
    def setUp(self):
        self.plano = Plano.objects.create(
            nome_plano="Fit Start",
            preco=89.90,
            modalidades_inclusas=1,
            duracao_meses=6,
        )
        self.admin = Administrador.objects.create(
            email="admin@academia.com",
            nome="Admin",
            is_staff=True,
            is_superuser=True,
        )
        self.admin.set_password("adminpass123")
        self.admin.save()

        self.funcionario = Funcionario.objects.create(
            email="func@academia.com",
            nome="Funcionario",
            id_funcionario="FUNC001",
        )
        self.funcionario.set_password("funcpass123")
        self.funcionario.save()

        self.aluno = Aluno.objects.create(
            email="aluno@academia.com",
            nome="Aluno",
            cpf="123.456.789-00",
            plano=self.plano,
        )
        self.aluno.set_password("alunopass123")
        self.aluno.save()

        self.outro_aluno = Aluno.objects.create(
            email="outro@academia.com",
            nome="Outro Aluno",
            cpf="987.654.321-00",
            plano=self.plano,
        )
        self.outro_aluno.set_password("outropass123")
        self.outro_aluno.save()

        self.modalidade_a = Modalidade.objects.create(
            modalidade_nome="Musculacao",
            categoria="Forca",
            horario="08:00",
            dias_semana=["Segunda", "Quarta"],
        )
        self.modalidade_b = Modalidade.objects.create(
            modalidade_nome="Pilates",
            categoria="Flexibilidade",
            horario="09:00",
            dias_semana=["Terca", "Quinta"],
        )

    def test_funcionario_nao_pode_editar_administrador_na_web(self):
        self.client.force_login(self.funcionario)
        response = self.client.get(f"/academia/usuarios/editar/{self.admin.id}/")
        self.assertContains(response, "Acesso negado")

    def test_aluno_registra_modalidade_respeitando_limite_do_plano(self):
        self.client.force_login(self.aluno)

        response = self.client.post(f"/modalidades/registrar/{self.modalidade_a.id}/", follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.aluno.refresh_from_db()
        self.assertEqual(self.aluno.modalidades_inscritas.count(), 1)

        response = self.client.post(f"/modalidades/registrar/{self.modalidade_b.id}/", follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.aluno.refresh_from_db()
        self.assertEqual(self.aluno.modalidades_inscritas.count(), 1)
        self.assertContains(response, "nao permite registrar mais modalidades")

    def test_aluno_lista_apenas_os_proprios_treinos(self):
        Treino.objects.create(
            nome_treino="Treino A",
            descricao="Treino do aluno logado",
            aluno=self.aluno,
            grupo_muscular="Peito",
            exercicios=["Supino"],
            series=3,
            repeticoes=12,
            data="2026-06-05",
        )
        Treino.objects.create(
            nome_treino="Treino B",
            descricao="Treino de outro aluno",
            aluno=self.outro_aluno,
            grupo_muscular="Costas",
            exercicios=["Remada"],
            series=4,
            repeticoes=10,
            data="2026-06-05",
        )

        self.client.force_login(self.aluno)
        response = self.client.get("/treinos/")
        self.assertContains(response, "Treino A")
        self.assertNotContains(response, "Treino B")

    def test_login_web_emite_cookies_jwt_e_autentica_api(self):
        response = self.client.post(
            "/api/academia/",
            {"email": self.admin.email, "password": "adminpass123"},
            follow=False,
        )

        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertIn("access_token", response.cookies)
        self.assertIn("refresh_token", response.cookies)
        self.assertFalse(response.cookies["access_token"]["secure"])
        self.assertFalse(response.cookies["refresh_token"]["secure"])

        api_response = self.client.get("/api/academia/alunos/")
        self.assertEqual(api_response.status_code, status.HTTP_200_OK)
