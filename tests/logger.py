import logging


_handler = logging.StreamHandler()
_format = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
_handler.setFormatter(_format)
logger = logging.getLogger('tests')
logger.addHandler(_handler)
