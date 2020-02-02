import json
from datetime import datetime
from hashlib import md5
from logging import Logger
from time import sleep

import requests

from domain.repositories.cache_repository import CacheRepository
from domain.models.mappa.login_response import Authentication
from infra.config import config
from infra.log import getLogger

_auth_data: Authentication = None

_cache = CacheRepository(config.CACHE_REPOSITORY)
_logger = getLogger("MAPPA")


class MappaService:

    USER_AGENT = "okhttp/3.4.1"

    def __init__(self):
        global _auth_data
        self.auth_data: Authentication = _auth_data
        self.logger: Logger = _logger
        self.cache: CacheRepository = _cache

    def authorization(self) -> str:
        return self.auth_data.userId

    @property
    def auth_data(self) -> Authentication:
        global _auth_data
        return _auth_data

    @auth_data.setter
    def auth_data(self, value: Authentication):
        global _auth_data
        _auth_data = value

    def auth_is_valid(self) -> bool:
        """ Returns true if authorization exists and is valid """
        return self.authorization() and \
            isinstance(self.auth_data.valid, datetime) and \
            self.auth_data.valid > datetime.now()

    def query(self, url: str, params: dict = None,
              ignoreCache: bool = False) -> dict:
        """ Returns dict or None from mAPPA query """
        if not self.auth_is_valid():
            self.logger.warning('MAPPA AUTHENTICATION ERROR')
            return None

        _headers = {
            "authorization": self.authorization(),
            "User-Agent": self.USER_AGENT,
            "Accept-Encoding": "gzip"
        }

        response = None
        urlkey = md5(f"{url}:{params}".encode('utf-8')).hexdigest()

        if not ignoreCache:
            response = self.cache.readCache(urlkey)
            if response is not None:
                self.logger.info(
                    "query(%s,%s) -> [cached] %s", url, params, response)
                return response

        count = 0
        success = False
        self.logger.info("query(%s,%s)", url, params)
        try_again = True

        while count < 5 and not success and try_again:
            count += 1
            try:
                ret = requests.get(url=config.MAPPA_BASE_URL + url,
                                   json=params,
                                   headers=_headers)
                if ret.status_code == 200:
                    response = json.loads(ret.content.decode('utf-8'))
                    self.cache.writeCache(urlkey, response)
                    success = True
                else:
                    self.logger.warning(
                        "status_code=%s: %s", ret.status_code, ret.text)

            except requests.exceptions.HTTPError as e:
                self.logger.exception("GET REQUEST %s", e)

            except UnicodeError as e:
                # Content is not UTF-8
                self.logger.exception("ENCODING ERROR %s", e)
                try_again = False

            except json.JSONDecodeError as e:
                # Invalid JSON content
                self.logger.exception(
                    "Invalid JSON content: %s: %s", ret.content, e)
                try_again = False

            if not success:
                if count < 5:
                    # Retrying
                    sleep(0.5)
                    self.logger.warning("Retrying")
                else:
                    self.logger.error("Exiting with failure")

            else:
                self.logger.info(response)

        return response

    def post(self, url: str, body: dict) -> dict:
        """ Returns dict or None from mAPPA POST query """
        _headers = {"User-Agent": self.USER_AGENT}
        self.logger.info('post(%s,%s)', url, body)
        response = None
        try:
            ret = requests.post(
                url=config.MAPPA_BASE_URL+url,
                json=body,
                headers=_headers)

            ret.raise_for_status()

            self.logger.info(ret.content)
            response = json.loads(ret.content)

        except Exception as e:
            self.logger.exception("POST %s", e)

        return response
