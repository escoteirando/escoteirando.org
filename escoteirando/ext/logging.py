from logging import Formatter, Logger, StreamHandler, getLogger
from logging.config import dictConfig

from flask import Flask

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})


_logger = None


def get_logger() -> Logger:
    global _logger
    if not _logger:
        _logger = getLogger('escoteirando')

    return _logger


def init_app(app: Flask):
    app.logger.addHandler(getLogger().handlers[0])
