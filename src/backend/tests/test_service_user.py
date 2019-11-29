import unittest
from domain.services.user_service import UserService
from domain.models.user import User


class TestUserService(unittest.TestCase):

    def test_instance(self):
        service = UserService()
        self.assertIsInstance(service, UserService)

    def test_set_logged_user(self):
        user = User(
            user_name="Guionardo",
            password="1234",
            level=0
        )
        service = UserService()
        service.set_logged_user(user)

        logged_user = service.get_logged_user()

        self.assertEqual(user, logged_user)

    def test_create_user(self):
        service = UserService()
        success, message = service.create_user("guionardo", "Abc123456")
        self.assertTrue(success, message)

    def test_get_user(self):
        service = UserService()
        user = service.get_user('guionardo')
        self.assertEqual(user.user_name, 'guionardo')
