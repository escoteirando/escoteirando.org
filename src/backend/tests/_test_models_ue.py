import unittest

from domain.models.ue.associado import Associado
from domain.models.ue.equipe import Equipe


class TestUEModels(unittest.TestCase):

    def test_equipe_model(self):
        equipe = Equipe(codigo_equipe=1)
        self.assertIsInstance(equipe, Equipe)

    def test_associado_model(self):
        equipe = Equipe(codigo_equipe=1)
        associado = Associado(
            codigo=1234, ds_nome="Guionardo Furlan", nr_registro='1234', equipe=equipe)
        self.assertIsInstance(associado, Associado)
