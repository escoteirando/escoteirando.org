import time

import requests
from dateutil.parser import parse

from escoteirando.ext.logging import get_logger

from .cache.cache import Cache
from .models.associado_response import Associado
from .models.escotista_response import Escotista
from .models.secao_response import Secao
from .models.grupo_response import Grupo
from .models.progressao_response import Progressao
from .models.login import Login
from .models.subsecao_response import Subsecao
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
        # Seção
        self.codigoSecao = None
        self.nomeSecao = None
        self.codigoTipoSecao = None
        self.subsecoes = []
        self.progressoes = []

    def __dict__(self):
        return {
            "authorization": self.authorization,
            "userId": self.userId,
            "userName": self.userName,
            "codigoAssociado": self.codigoAssociado,
            # Escotista
            "codigoGrupo": self.codigoGrupo,
            "nomeGrupo": self.nomeGrupo,
            "codigoRegiao": self.codigoRegiao,
            "codigoFoto": self.codigoFoto,
            # Associado
            "codigoEquipe": self.codigoEquipe,
            "dataNascimento": self.dataNascimento,
            "sexo": self.sexo,
            "codigoRamo": self.codigoRamo,
            "linhaFormacao": self.linhaFormacao,
            # Seção
            "codigoSecao": self.codigoSecao,
            "nomeSecao": self.nomeSecao,
            "codigoTipoSecao": self.codigoTipoSecao,
            "subsecoes": self.subsecoes,
            "progressoes": self.progressoes
        }

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
                if self.get_grupo(self.codigoGrupo, self.codigoRegiao):
                    if self.get_secao(self.userId):
                        self.get_subsecoes(self.userId, self.codigoSecao)

        self.get_progressoes()

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

    def get_associado(self, userId) -> Associado:
        code, response = self.http.get(f"/api/associados/{userId}")
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

    def get_secao(self, userId) -> Secao:
        http_code, response = self.http.get(
            f'/api/escotistas/{userId}/secoes')
        ret: Secao = None if http_code >= 300 else Secao(response)
        if ret:
            self.codigoSecao = ret.codigo
            self.nomeSecao = ret.nome
            self.codigoTipoSecao = ret.codigoTipoSecao

        return ret

    def get_subsecoes(self, userId, codigoSecao) -> list:
        filter = {"filter": {"include": "associados"}}
        http_code, response = self.http.get(
            f'/api/escotistas/{userId}/secoes/{codigoSecao}/equipes', params=filter)

        ret = None if http_code >= 300 else response

        subsecoes = []

        if isinstance(ret, list):
            for subsec in ret:
                subsecoes.append(Subsecao(subsec))

            self.subsecoes = subsecoes

        return subsecoes

    def get_progressoes(self):
        filter = {"filter":
                  {"where":        {
                      "numeroGrupo": None,
                      "codigoRegiao": None,
                      "codigoCaminho": {"inq": [1, 2, 3, 4, 5, 6, 11, 12, 15, 16]}
                  }}}
        http_code, result = self.http.get(
            '/api/progressao-atividades', params=filter)

        ret = None if http_code >= 300 else result

        progressoes = []
        if ret and isinstance(ret, list):
            for progressao in result:
                progressoes.append(Progressao(progressao))

        self.progressoes = progressoes

        return progressoes
