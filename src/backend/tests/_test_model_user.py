import unittest
from domain.models.user import User
#from domain.models.ue.associado import Associado


class TestUserModel(unittest.TestCase):

    def test_user_model(self):
        user = User(user_name="Guionardo")
        #associado = Associado(codigo=1234, nome="Guionardo Furlan")
        #user.associado = associado
        self.assertIsInstance(user, User)
        self.assertEqual(user.user_name, "Guionardo")
        d = user.__dict__()
        self.assertEqual(d["user_name"], "Guionardo")
