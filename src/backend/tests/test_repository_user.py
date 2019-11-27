import unittest
from datetime import datetime

from domain.models import User
from domain.models.ue.associado import Associado
from domain.repositories import UserRepository, UERepository


class TestUserRepository(unittest.TestCase):
    repo = UserRepository()
    ue_repo = UERepository()

    def test_instance(self):
        self.assertIsInstance(self.repo, UserRepository)

    def test_post(self):
        associado = self.ue_repo.get_associado(1)
        if associado is None:
            associado = Associado(codigo=1, ds_nome="Guionardo Furlan",
                                  nr_registro=1)

        user = User(user_name="guionardo", associado=associado,
                    password="1234", level=2)
        self.assertTrue(self.repo.post(user))

    def test_get(self):
        user: User = self.repo.get('guionardo')
        self.assertIsInstance(user, User)
        self.assertEqual(user.user_name, 'guionardo')
