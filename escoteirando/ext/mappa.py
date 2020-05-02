from mappa.service.mappa_service import MAPPAService

from .configs import Configs


def init_app(app):
    c = Configs.Instance()
    app.mappa = MAPPAService(c.CACHE_STRING_CONNECTION)
