from datetime import datetime

from flask import abort, current_app, jsonify
from flask_login import current_user
from flask_restful import Resource

from escoteirando.domain.models.notificacao import Notificacao
from escoteirando.ext.logging import getLogger

from .auth import should_be_logged

logger = getLogger()


def setup_notificacoes(api):
    api.add_resource(NotificacaoResource, "/notificacoes/<int:id_usuario>")


class NotificacaoResource(Resource):

    def get(self, id_usuario):
        should_be_logged()

        notificacoes = Notificacao.query.filter_by(id_usuario=id_usuario)
        vencidas = [
            notificacao.id for notificacao in notificacoes if notificacao.valida_ate < datetime.utcnow()]
        if vencidas:
            for id in vencidas:
                Notificacao.query.filter(Notificacao.id == id).delete()
            current_app.db.session.commit()

        result = [{
            "msg": notificacao.mensagem,
            "id": notificacao.id,
            "link": notificacao.link}
            for notificacao in notificacoes
            if notificacao.id not in vencidas]
        return jsonify(result)

    def delete(self, id_usuario):
        notificacao = Notificacao.query.filter_by(id=id_usuario).first()
        if not notificacao:
            return "NOT FOUND", 404

        should_be_logged(notificacao.id_usuario)
        notificacao.delete()
        current_app.db.session.commit()
        return "OK", 200
