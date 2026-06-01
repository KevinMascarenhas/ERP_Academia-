from django.test import TestCase
from planos.models import Plano

class PlanoModelTestCase(TestCase):
    def test_plano_creation_and_str(self):
        plano = Plano.objects.create(
            nome_plano="Gold",
            preco=99.90,
            modalidades_inclusas=2,
            duracao_meses=6
        )
        self.assertEqual(plano.nome_plano, "Gold")
        self.assertEqual(float(plano.preco), 99.90)
        self.assertEqual(plano.modalidades_inclusas, 2)
        self.assertEqual(plano.duracao_meses, 6)
        self.assertEqual(str(plano), "Gold — R$ 99.90/mês")
