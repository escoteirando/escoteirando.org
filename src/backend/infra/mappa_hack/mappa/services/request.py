import json
from time import sleep

import requests

from .cache import Cache

_authorization = None
_cache = Cache()
_url = "http://mappa.escoteiros.org.br"


class HTTP:
    OK = 200
    UNAUTHORIZED = 401
    SERVER_ERROR = 500

    def __init__(self, cachePath: str, baseUrl: str):
        self._cache = Cache(cachePath)
        self._url = baseUrl
        self._authorization = None

    def setAuthorization(self, authorization: str):
        self._authorization = authorization

    def get(self, url: str, params: dict = None, description: str = None, gzipped: bool = False):
        description = url if not description else description
        if not _authorization:
            return HTTP.UNAUTHORIZED, 'UNAUTHORIZED'

        _headers = {
            "authorization": _authorization,
            "User-Agent": "okhttp/3.4.1"
        }
        if gzipped:
            _headers["Accept-Encoding"] = "gzip"

        cached = self._cache.readCache(url, _headers)
        if cached:
            return HTTP.OK, cached

        count = 0
        success = False
        exceptions = []

        while count < 5 and not success:
            count += 1
            try:
                ret = requests.get(_url+url, json=params, headers=_headers)
                if ret.status_code == HTTP.OK:
                    content = ret.content.decode('utf-8')
                    self._cache.writeCache(url, content, _headers)
                    return HTTP.OK, json.loads(content)
                else:
                    return ret.status_code, json.loads(ret.text)
            except Exception as e:
                if str(e) not in exceptions:
                    exceptions.append(str(e))
                if count < 5:
                    sleep(1)

        return HTTP.SERVER_ERROR, exceptions[0]

    def post(self, url: str, params: dict):
        try:
            _headers = {
                "User-Agent": "okhttp/3.4.1"
            }
            ret = requests.post(_url+url, json=params, headers=_headers)
            if ret.status_code == HTTP.OK:
                return ret.status_code, json.loads(ret.content)
            else:
                return ret.status_code, ret.text
        except Exception as e:
            return HTTP.SERVER_ERROR, str(e)
