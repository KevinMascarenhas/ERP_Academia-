from django.test import TestCase
from django.contrib.auth import get_user_model
from academia.models import Usuario, Administrador, Funcionario, Aluno
from planos.models import Plano

class AcademiaModelsTestCase(TestCase):
    def setUp(self):
        self.plano_ouro = Plano.objects.create(
            nome_plano="Ouro",
            preco=150.00,
            modalidades_inclusas=3,
            duracao_meses=12
        )

    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(
            email="test@user.com",
            nome="Test User",
            password="securepassword123"
        )
        self.assertEqual(user.email, "test@user.com")
        self.assertEqual(user.nome, "Test User")
        self.assertEqual(user.perfil, "Administrador")
        self.assertTrue(user.check_password("securepassword123"))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(
            email="admin@user.com",
            nome="Admin User",
            password="adminpassword123"
        )
        self.assertEqual(admin_user.email, "admin@user.com") # assert é um metodo de verificação, ele compara o valor esperado com o valor real e retorna um erro se eles não forem iguais.
        self.assertEqual(admin_user.perfil, "Administrador")
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)

    def test_administrador_profile_auto_assignment(self):
        admin = Administrador.objects.create(
            email="adm@academia.com",
            nome="Carlos Admin"
        )
        self.assertEqual(admin.perfil, Usuario.PERFIL_ADMIN)

    def test_funcionario_profile_auto_assignment(self):
        func = Funcionario.objects.create(
            email="func@academia.com",
            nome="Ana Func",
            id_funcionario="FUNC001"
        )
        self.assertEqual(func.perfil, Usuario.PERFIL_FUNCIONARIO)
        self.assertEqual(func.id_funcionario, "FUNC001")

    def test_aluno_profile_auto_assignment(self):
        aluno = Aluno.objects.create(
            email="aluno@academia.com",
            nome="Joao Aluno",
            cpf="123.456.789-00",
            plano=self.plano_ouro
        )
        self.assertEqual(aluno.perfil, Usuario.PERFIL_ALUNO)
        self.assertEqual(aluno.cpf, "123.456.789-00")
        self.assertEqual(aluno.plano, self.plano_ouro)
