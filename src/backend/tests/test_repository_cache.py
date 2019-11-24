import os
import unittest

from domain.repositories.cache_repository import CacheRepository


class TestCacheRepository(unittest.TestCase):

    def test_file_cache(self):
        source = os.path.realpath('.cache')
        if not os.path.isdir(source):
            os.makedirs(source)
        cache = CacheRepository(source)
        self.assertTrue(cache.writeCache('http://localhost/test', 'conteudo'))
