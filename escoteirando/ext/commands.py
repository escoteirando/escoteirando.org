import click
from escoteirando.ext.database import db
from escoteirando.ext.auth import create_user
from escoteirando.models.product import Product
from escoteirando.domain.models.mappa import MAPPA_Progressao
from escoteirando.domain.models.atividade import Atividade
from escoteirando.domain.models.encontro import Encontro
from escoteirando.domain.models.grupo_escoteiro import GrupoEscoteiro

from flask_migrate import Migrate, MigrateCommand


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


def init_app(app):
    # add multiple commands in a bulk
    for command in [create_db, drop_db, populate_db]:
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
