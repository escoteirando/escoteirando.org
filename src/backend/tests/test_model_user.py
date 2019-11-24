import unittest
from domain.models.user import User


class TestUserModel(unittest.TestCase):

    def test_user_model(self):
        user = User(user_name="Guionardo")
        self.assertIsInstance(user, User)
        self.assertEqual(user.user_name, "Guionardo")
        d = user.__dict__()
        self.assertEqual(d["user_name"], "Guionardo")
