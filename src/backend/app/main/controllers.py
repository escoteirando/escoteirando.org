from flask import Blueprint, render_template
from app.auth.controllers import LoggedUser

main = Blueprint('main', __name__,template_folder='pages')


@main.route('/')
def index():
    user = LoggedUser.getUser()
    if user is None:
        return render_template('index_logged_out.html')
        
    
