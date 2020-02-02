import logging
from infra.config import config

_loggers = {}

FORMAT = ('%(asctime)s %(levelname)s [%(name)s] [%(filename)s:%(lineno)d] '
          '- %(message)s')

logging.basicConfig(format=FORMAT,
                    level=logging.INFO
                    if config.FLASK_ENV == 'production'
                    else logging.DEBUG)


def getLogger(module) -> logging.Logger:
    if module not in _loggers:
        c_handler = logging.StreamHandler()
        c_format = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        c_handler.setFormatter(c_format)
        logger = logging.getLogger(module)
        logger.addHandler(c_handler)
        _loggers[module] = logger

    return _loggers[module]
