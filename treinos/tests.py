from django.test import TestCase
from django.utils import timezone
from academia.models import Aluno
from planos.models import Plano
from treinos.models import Treino

class TreinosTestCase(TestCase):
    def setUp(self):
        self.plano = Plano.objects.create(
            nome_plano="Plano Treino",
            preco=100.00,
            modalidades_inclusas=1,
            duracao_meses=1
        )
        self.aluno = Aluno.objects.create(
            email="alunotreino@academia.com",
            nome="Pedro Treino",
            cpf="111.222.333-44",
            plano=self.plano
        )

    def test_treino_creation(self):
        hoje = timezone.now().date()
        treino = Treino.objects.create(
            nome_treino="Treino de Hipertrofia A",
            descricao="Foco em membros superiores",
            aluno=self.aluno,
            grupo_muscular="Peito e Tríceps",
            exercicios=[
                {"nome": "Supino Reto", "series": 4, "repeticoes": 10},
                {"nome": "Tríceps Pulley", "series": 3, "repeticoes": 12}
            ],
            series=4,
            repeticoes=10,
            data=hoje
        )
        self.assertEqual(treino.nome_treino, "Treino de Hipertrofia A")
        self.assertEqual(treino.aluno, self.aluno)
        self.assertEqual(treino.grupo_muscular, "Peito e Tríceps")
        self.assertEqual(len(treino.exercicios), 2)
        self.assertEqual(treino.exercicios[0]["nome"], "Supino Reto")
        self.assertEqual(treino.series, 4)
        self.assertEqual(treino.repeticoes, 10)
        self.assertEqual(treino.data, hoje)
        self.assertIn("Pedro Treino", str(treino))
