from flask_sqlalchemy import SQLAlchemy
from .service_infra import ServiceInfra


class ServiceAdmin:

    def __init__(self, db: SQLAlchemy):
        self.DB: SQLAlchemy = db
        self.service_infra = ServiceInfra(db)

    def send_email(self, to: str, subject: str, content: str):
        # TODO: Enviar email
        pass
