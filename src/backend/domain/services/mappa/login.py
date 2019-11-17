from datetime import datetime

from domain.models.mappa.login_response import Authentication
from domain.repositories.cacherepository import CacheRepository
from domain.services.mappa.request import authIsValid, post, setAuth
from infra.config import config
from infra.log import getLogger

logger = getLogger("login")
_cache = CacheRepository(config.CACHE)


def login(username, password):
    keylogin = f"auth:{username}:{password}"
    cachedLogin = _cache.readCache(keylogin)
    if cachedLogin:
        auth = Authentication(cachedLogin)
        if auth.valid > datetime.now():
            logger.info(f"login({username}) FROM CACHE")
            setAuth(auth.id, auth.valid)

    if authIsValid():
        logger.info(f"login({username}) PRE-AUTHORIZED OK")
        return True

    login_response = post(
        url='/api/escotistas/login',
        body={"type": "LOGIN_REQUEST",
              "username": username,
              "password": password})

    if login_response:
        auth = Authentication(login_response)
        setAuth(auth.id, auth.valid)
        _cache.writeCache(keylogin, auth.__dict__)
        logger.info(f'login({username}) POST-AUTHORIZED OK')
        return True

    logger.error(f'login({username}) NOT AUTHORIZED')
    return False
