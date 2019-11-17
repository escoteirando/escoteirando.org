import logging

_loggers = {}


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
