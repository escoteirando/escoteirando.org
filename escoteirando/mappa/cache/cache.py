import hashlib
import logging
import os
from glob import glob, iglob
from time import time

from .cache_item import CacheItem


class Cache:
    """ Cache control of objects with age """

    def __init__(self, path, logger: logging.Logger, purge_interval: int = 60):
        """ Initialize cache.

        :param: path of cache str

        :logger: logging.Logger

        :purge_interval: automatic purge interval in seconds
        """
        if not isinstance(path, str) or not path:
            raise ValueError('Cache: path must be str')
        if not isinstance(logger, logging.Logger):
            raise ValueError('Cache: logger must be Logger')

        self.logger = logger

        path = os.path.abspath(path)

        if not os.path.isdir(path):
            try:
                os.makedirs(path)
                self.logger.info('Cache: create folder %s', path)
            except OSError as path_exc:
                self.logger.exception(
                    'Cache: error on create folder %s', path_exc)
                raise

        self.path = path
        self.logger.info('Cache initialized in %s', self.path)
        self.purge_interval = purge_interval
        self.last_purge = 0

    def get(self, key: str, default_value=None):
        filename = self._key_file(key)
        if os.path.isfile(filename):
            ci = CacheItem(filename)
            if ci.valid:
                return ci.payload
        return default_value

    def set(self, key: str, value, max_age: int = 0):
        filename = self._key_file(key)
        if not os.path.isdir(os.path.dirname(filename)):
            os.makedirs(os.path.dirname(filename))

        CacheItem(filename).set(payload=value, max_age=max_age).save()
        self.auto_purge()

    def delete(self, key: str):
        filename = self._key_file(key)
        if os.path.isfile(filename):
            os.unlink(filename)

    def auto_purge(self):
        if self.purge_interval > 0 and time()-self.last_purge > self.purge_interval:
            self.purge()
            self.last_purge = time()

    def purge(self):
        removed = 0
        try:
            for l1 in glob(os.path.join(self.path, '??')):
                if not os.path.isdir(l1):
                    continue
                for l2 in glob(os.path.join(l1, '??')):
                    if not os.path.isdir(l2):
                        continue
                    for cf in iglob(os.path.join(l2, '*.cache')):
                        if not os.path.isfile(cf):
                            continue
                        removed += 1 if CacheItem(cf,
                                                  just_validate=True).valid else 0
        except Exception as exc:
            self.logger.exception('Purge cache exception: %s', exc)
        self.logger.info('Purge cache: removed %s files', removed)

    def _key_file(self, key: str):
        hash = hashlib.md5(key.encode()).hexdigest()
        path = os.path.join(self.path, hash[:2], hash[2:4], hash+'.cache')
        return path
