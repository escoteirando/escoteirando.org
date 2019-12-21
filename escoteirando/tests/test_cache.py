from escoteirando.mappa.cache.cache import Cache
from escoteirando.mappa.cache.cache_item import CacheItem
from .logger import logger
from time import time
from datetime import datetime
import os


def test_cache_item():
    ci = CacheItem('test.cache').set('CONTENT', time()+30).save()
    assert os.path.isfile('test.cache')
    os.unlink('test.cache')


def test_cache():
    cache = Cache('.cache', logger)
    value = {'id': 1, 'name': 'Guionardo', 'today': datetime.now()}
    #cache.set('teste', value, time()+30)

    #v2 = cache.get('teste')
    #assert value == v2

    cache.purge()
