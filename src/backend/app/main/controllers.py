from flask import Blueprint, render_template
from domain.services.user_service import userService as UserService

main = Blueprint('main', __name__, template_folder='pages')


@main.route('/')
def index():
    us = UserService()
    user = us.get_logged_user()
    if user is None:
        return render_template('main/login.html',
                               title="Login",
                               body_class="text-center")
    else:
        return render_template('main/index.html',
                               title="Atividades")
        # return render_template('index_logged_out.html')
