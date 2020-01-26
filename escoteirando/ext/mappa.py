from escoteirando.mappa.mappa import Mappa


def init_app(app):
    app.mappa = Mappa('.cache')
