import time

import requests
from dateutil.parser import parse

from escoteirando.ext.logging import get_logger

from .cache.cache import Cache
from .models.associado_response import Associado
from .models.escotista_response import Escotista
from .models.grupo_response import Grupo
from .models.login import Login
from .request import HTTP


class Mappa:

    def __init__(self, cache_path):
        self.logger = get_logger()
        self.cache = Cache(cache_path, logger=self.logger)
        self.http = HTTP(cache=self.cache)
        self.authorization = None
        self.userId = None
        self.userName = None
        self.codigoAssociado = None
        # Escotista
        self.codigoGrupo = None
        self.codigoRegiao = None
        self.codigoFoto = None
        # Associado
        self.codigoEquipe = None
        self.dataNascimento = None
        self.sexo = None
        self.codigoRamo = None
        self.linhaFormacao = None
        # Grupo
        self.nomeGrupo = None

    def login(self, username, password) -> bool:
        response = self.cache.get('login', username)
        if response:
            login = Login(response)
            self.logger.info('login user (%s) from cache', username)
        else:
            code, response = self.http.post(
                url='/api/escotistas/login',
                params={"type": "LOGIN_REQUEST",
                        "username": username,
                        "password": password})
            if code != 200:
                self.logger.warning('login user (%s) failed', username)
                return False
            login = Login(response)
            if login.ttl:
                max_age = time.time()+login.ttl
                self.cache.set(key='login', value=dict(
                    response), max_age=max_age, options=username)
                self.logger.info('login user (%s) from MAPPA', username)
            else:
                self.logger.warning('login user (%s) failed: TTL unidentified')
                return False
        self.authorization = login.id
        self.userId = login.userId
        self.http.setAuthorization(login.id)

        if self.get_escotista(self.userId):
            if self.get_associado(self.codigoAssociado):
                self.get_grupo(self.codigoGrupo, self.codigoRegiao)
        return True

    def get_escotista(self, userId) -> Escotista:
        """ Retorna o escotista do usuário

        :param userId: userId obtido a partir do Login
        """

        code, response = self.http.get(f'/api/escotistas/{userId}')
        ret: Escotista = None if code >= 300 else Escotista(response)
        if ret:
            self.codigoAssociado = ret.codigoAssociado
            self.codigoFoto = ret.codigoFoto
            self.codigoGrupo = ret.codigoGrupo
            self.codigoRegiao = ret.codigoRegiao

        return ret

    def get_associado(self, codigoAssociado) -> Associado:
        code, response = self.http.get(f"/api/associados/{codigoAssociado}")
        ret: Associado = None if code >= 300 else Associado(response)
        if ret:
            self.codigoEquipe = ret.codigoEquipe
            self.dataNascimento = parse(ret.dataNascimento)
            self.sexo = ret.sexo
            self.codigoRamo = ret.codigoRamo
            self.linhaFormacao = ret.linhaFormacao

        return ret

    def get_grupo(self, codigo, codigoRegiao) -> Grupo:
        filter = {
            "filter": {
                "where": {
                    "codigo": codigo,
                    "codigoRegiao": codigoRegiao
                }
            }
        }
        http_code, response = self.http.get('/api/grupos', params=filter)
        ret: Grupo = None if http_code >= 300 else Grupo(response)
        if ret:
            self.nomeGrupo = ret.nome

        return ret
