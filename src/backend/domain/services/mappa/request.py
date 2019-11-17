import json
from datetime import datetime
from hashlib import md5
from time import sleep

import requests

from domain.repositories.cacherepository import CacheRepository
from infra.config import config
from infra.log import getLogger

_authorization = None
_validUntil = None
_baseURL = config.MAPPA_BASE_URL
_cache = CacheRepository(config.CACHE)
logger = getLogger('request')



def setAuth(authorization: str, validUntil: datetime):
    """ Defines authorization for queries """
    global _authorization, _validUntil
    _authorization = authorization
    _validUntil = validUntil    
    logger.info(f"setAuth({authorization},{validUntil})")


def authIsValid():
    """ Checks if authorization is valid """
    return (_authorization is not None) and (_validUntil > datetime.now())


def query(url: str, params: dict = None, ignoreCache: bool = False) -> dict:
    """ Returns dict or None from mAPPA query """
    if not authIsValid():
        return None

    _headers = {
        "authorization": _authorization,
        "User-Agent": "okhttp/3.4.1",
        "Accept-Encoding": "gzip"
    }

    response = None
    urlkey = md5(url+str(params)).hexdigest()

    if not ignoreCache:
        cache = CacheRepository(config.CACHE)
        response = cache.readCache(urlkey)
        if response is not None:
            logger.info(f"query({url},{params}) -> [cached] {response}")
            return response

    count = 0
    success = False
    logger.info(f"query({url},{params})")
    try_again = True

    while count < 5 and not success and try_again:
        count += 1
        try:
            ret = requests.get(url=_baseURL + url,
                               json=params,
                               headers=_headers)
            if ret.status_code == 200:
                response = json.loads(ret.content.decode('utf-8'))
                cache.writeCache(urlkey, response)
                success = True
            else:
                logger.warning(f"status_code={ret.status_code}: {ret.text}")

        except requests.exceptions.HTTPError as e:
            logger.error(str(e))

        except UnicodeError as e:
            # Content is not UTF-8
            logger.error(str(e))
            try_again = False

        except json.JSONDecodeError as e:
            # Invalid JSON content
            logger.warning(f"Invalid JSON content: {ret.content}")
            try_again = False

        if not success:
            if count < 5:
                # Retrying
                sleep(0.5)
                logger.warning("Retrying")
            else:
                logger.error("Exiting with failure")

        else:
            logger.info(response)

    return response


def post(url: str, body: dict) -> dict:
    """ Returns dict or None from mAPPA POST query """
    _headers = {
        "User-Agent": "okhttp/3.4.1"
    }
    logger.info(f'post({url},{body})')
    response = None
    try:
        ret = requests.post(
            url=_baseURL+url,
            json=body,
            headers=_headers)

        ret.raise_for_status()

        logger.info(ret.content)
        response = json.loads(ret.content)

    except Exception as e:
        logger.error(str(e))

    return response
