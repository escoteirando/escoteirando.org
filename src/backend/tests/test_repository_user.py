import unittest
from domain.repositories.user_repository import UserRepository, User


class TestUserRepository(unittest.TestCase):

    def test_get(self):
        user: User = UserRepository().get('guionardo')
        self.assertIsInstance(user, User)
        self.assertEqual(user.user_name, 'guionardo')
