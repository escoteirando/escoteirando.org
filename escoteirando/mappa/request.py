import json
from time import sleep, time

import requests

from .cache.cache import Cache
from escoteirando.ext.logging import get_logger


class HTTP:
    OK = 200
    UNAUTHORIZED = 401
    SERVER_ERROR = 500

    def __init__(self, cachePath: str = None, cache: Cache = None):
        self._url = "http://mappa.escoteiros.org.br"
        self._authorization = None
        self.logger = get_logger()
        if cachePath:
            self._cache = Cache(cachePath, self.logger)
        elif cache:
            self._cache = cache
        else:
            raise ValueError('cache not informed')

    def setAuthorization(self, authorization: str):
        self._authorization = authorization

    def get(self, url: str, params: dict = None, description: str = None, gzipped: bool = False) -> tuple:
        ''' HTTP GET

        :param url:
        :param params:

        :return: tuple (http_code, content)
        '''
        description = url if not description else description
        if not self._authorization:
            return HTTP.UNAUTHORIZED, 'UNAUTHORIZED'

        _headers = {
            "authorization": self._authorization,
            "User-Agent": "okhttp/3.4.1"
        }
        if gzipped:
            _headers["Accept-Encoding"] = "gzip"

        cached = self._cache.get(url, options=_headers)
        if cached:
            return HTTP.OK, cached

        count = 0
        success = False
        exceptions = []

        while count < 5 and not success:
            count += 1
            try:
                ret = requests.get(
                    self._url+url, json=params, headers=_headers)
                if ret.status_code == HTTP.OK:
                    content = ret.content.decode('utf-8')
                    self._cache.set(
                        url, content, max_age=time()+172800, options=_headers)
                    return HTTP.OK, json.loads(content)
                else:
                    return ret.status_code, json.loads(ret.text)
            except Exception as e:
                if str(e) not in exceptions:
                    exceptions.append(str(e))
                if count < 5:
                    sleep(1)

        return HTTP.SERVER_ERROR, exceptions[0]

    def post(self, url: str, params: dict) -> tuple:
        """ Send POST request to MAPPA API.

        :param url: url path (p.ex '/login')
        :param params: json body
        :returns: (status_code, dict/str)
        """
        try:
            _headers = {
                "User-Agent": "okhttp/3.4.1"
            }
            ret = requests.post(self._url+url, json=params, headers=_headers)
            if ret.status_code == HTTP.OK:
                return ret.status_code, json.loads(ret.content)
            else:
                return ret.status_code, ret.text
        except Exception as e:
            return HTTP.SERVER_ERROR, str(e)
