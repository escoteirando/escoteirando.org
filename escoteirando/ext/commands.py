import click
from flask_migrate import Migrate, MigrateCommand

from escoteirando.domain.models.atividade import Atividade
from escoteirando.domain.models.db.associado import Associado
from escoteirando.domain.models.db.secao import Secao
from escoteirando.domain.models.encontro import Encontro
from escoteirando.domain.models.encontro_atividade import EncontroAtividade
from escoteirando.domain.models.encontro_escotistas import EncontroEscotista
from escoteirando.domain.models.grupo_escoteiro import GrupoEscoteiro
from escoteirando.domain.models.infra.params import Param
from escoteirando.domain.models.notificacao import Notificacao
from escoteirando.domain.models.user import User
from escoteirando.ext.auth import create_user
from escoteirando.ext.database import db
from escoteirando.models.product import Product


def create_db():
    """Creates database"""
    db.create_all()
    create_user('admin', 'admin')


def drop_db():
    """Cleans database"""
    db.drop_all()


def populate_db():
    """Populate db with sample data"""
    data = [
        Product(
            id=1, name="Ciabatta", price="10", description="Italian Bread"
        ),
        Product(id=2, name="Baguete", price="15", description="French Bread"),
        Product(id=3, name="Pretzel", price="20", description="German Bread"),
    ]
    db.session.bulk_save_objects(data)
    db.session.commit()
    return Product.query.all()


def add_admin():
    """Adds a new user to the database"""
    return create_user('admin', 'admin')


def init_app(app):
    # add multiple commands in a bulk
    for command in [create_db, drop_db, populate_db, add_admin]:
        app.cli.add_command(app.cli.command()(command))

    migrate = Migrate(app, db)
    # Migrations
    app.cli.add_command('db', MigrateCommand)
    # add a single command
    @app.cli.command()
    @click.option('--username', '-u')
    @click.option('--password', '-p')
    def add_user(username, password):
        """Adds a new user to the database"""
        return create_user(username, password)

    print('Commands added')
