import os
import unittest

from domain.repositories.cache_repository import CacheRepository
from infra.config import config


class TestCacheRepository(unittest.TestCase):

    url = 'http://localhost/test'
    content = 'conteudo'

    def test_file_cache(self):
        source = os.path.realpath('.cache')
        if not os.path.isdir(source):
            os.makedirs(source)
        cache = CacheRepository(source)

        self.assertTrue(cache.writeCache(self.url, self.content))
        self.assertEqual(cache.readCache(self.url).content, self.content)

    def test_mongo_cache(self):
        cache = CacheRepository(
            config.MONGODB_URL+'/'+config.MONGODB_DB+'/cache')

        self.assertTrue(cache.writeCache(self.url, self.content))
        self.assertEqual(cache.readCache(self.url).content, self.content)
