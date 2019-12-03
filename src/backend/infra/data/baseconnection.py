from logging import Logger

from infra.log import getLogger

logger = getLogger('mongodb')


class BaseConnection:

    @property
    def logger(self) -> Logger:
        return logger
