from . import BaseModel
from infra.login import login_manager
from flask_login import UserMixin
from domain.repositories import UsersRepository
class User(BaseModel,UserMixin):

    def __init__(self, fromDict=None):
        self.id = None
        self.user_name = None
        super().__init__(fromDict)
        

@login_manager.user_loader
def load_user(user_id):
    return UsersRepository().get(user_id)