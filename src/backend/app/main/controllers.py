from flask import Blueprint, render_template
from domain.services.user_service import UserService

main = Blueprint('main', __name__, template_folder='pages')
user_service = UserService()


@main.route('/')
def index():
    user = user_service.get_logged_user()
    if user is None:
        return render_template('index_logged_out.html')
