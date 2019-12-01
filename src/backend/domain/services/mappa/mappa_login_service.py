from datetime import datetime

from domain.models.mappa.associado_response import Associado
from domain.models.mappa.escotista_response import Escotista
from domain.models.mappa.grupo_response import Grupo
from domain.models.mappa.login_response import Authentication

from .mappa_base_service import MappaService


class MappaLoginService(MappaService):

    def login(self, username, password):
        keylogin = f"auth:{username}:{password}"
        cachedLogin = self.cache.readCache(keylogin)

        if cachedLogin:
            auth = Authentication(cachedLogin)
            if auth.valid > datetime.now():
                self.logger.info("login(%s) FROM CACHE", username)
                self.auth_data = auth

        if self.auth_is_valid():
            self.logger.info("login(%s) PRE-AUTHORIZED OK", username)
            return True

        login_response = self.post(
            url='/api/escotistas/login',
            body={"type": "LOGIN_REQUEST",
                  "username": username,
                  "password": password})

        if login_response:
            self.auth_data = Authentication(login_response)
            self.cache.writeCache(keylogin, auth.__dict__)
            self.logger.info(f'login({username}) POST-AUTHORIZED OK')
            return True

        self.logger.error(f'login({username}) NOT AUTHORIZED')
        return False

    def get_escotista(self, userId) -> Escotista:
        """                
GET /api/escotistas/50442 HTTP/1.1
accept: application/json
cache-control: no-cache
authorization: q9yAbpHAjAsqsf7J8U9dhmuva8p7asafG3nqygYF9PBWi2d3B2OCLMoCXds2wgfg
Host: mappa.escoteiros.org.br
Connection: Keep-Alive
Accept-Encoding: gzip
User-Agent: okhttp/3.4.1

HTTP/1.1 200 OK
Vary: Origin, Accept-Encoding
Access-Control-Allow-Credentials: true
X-XSS-Protection: 1; mode=block
X-Frame-Options: DENY
X-Download-Options: noopen
X-Content-Type-Options: nosniff
Content-Type: application/json; charset=utf-8
Content-Length: 164
ETag: W/"a4-QbR9upz5WMuxrcRCTO8ThrPpp2M"
Date: Sat, 26 Oct 2019 02:19:09 GMT

{"codigo":50442,"codigoAssociado":850829,"username":"Guionardo","nomeCompleto":"GuionardoFurlan","ativo":"S","codigoGrupo":32,"codigoRegiao":"SC","codigoFoto":null}
        """

        response = self.query(f'/api/escotistas/{userId}')
        return None if response is None else Escotista(response.content)

    def get_associado(self, codigoAssociado) -> Associado:
        '''
GET /api/associados/850829 HTTP/1.1
accept: application/json
cache-control: no-cache
authorization: q9yAbpHAjAsqsf7J8U9dhmuva8p7asafG3nqygYF9PBWi2d3B2OCLMoCXds2wgfg
Host: mappa.escoteiros.org.br
Connection: Keep-Alive
Accept-Encoding: gzip
User-Agent: okhttp/3.4.1

HTTP/1.1 200 OK
Vary: Origin, Accept-Encoding
Access-Control-Allow-Credentials: true
X-XSS-Protection: 1; mode=block
X-Frame-Options: DENY
X-Download-Options: noopen
X-Content-Type-Options: nosniff
Content-Type: application/json; charset=utf-8
Content-Length: 413
ETag: W/"19d-Ymko+aAa2XJu5XHkS83jwZl1xLY"
Date: Sat, 26 Oct 2019 02:19:09 GMT

{
    "codigo":850829,
    "nome":"GUIONARDO FURLAN",
    "codigoFoto":null,
    "codigoEquipe":null,
    "username":1247937,
    "numeroDigito":3,
    "dataNascimento":"Sat Feb 05 1977 00:00:00 GMT+0000 (UTC)",
    "dataValidade":"2019-01-01T00:00:00.000Z",
    "nomeAbreviado":"",
    "sexo":"M",
    "codigoRamo":2,
    "codigoCategoria":5,
    "codigoSegundaCategoria":0,
    "codigoTerceiraCategoria":0,
    "linhaFormacao":"Escotista",
    "codigoRamoAdulto":2,
    "dataAcompanhamento":null
    }
    '''

        response = self.query(f'/api/associados/{codigoAssociado}')
        return None if response is None else Associado(response.content)

    def get_grupo(self, codigo, codigoRegiao):
        """
GET /api/grupos?filter={%22where%22:%20{%22codigo%22:%2032,%20%22codigoRegiao%22:%20%22SC%22}} HTTP/1.1
accept: application/json
cache-control: no-cache
authorization: q9yAbpHAjAsqsf7J8U9dhmuva8p7asafG3nqygYF9PBWi2d3B2OCLMoCXds2wgfg
Host: mappa.escoteiros.org.br
Connection: Keep-Alive
Accept-Encoding: gzip
User-Agent: okhttp/3.4.1

HTTP/1.1 200 OK
Vary: Origin, Accept-Encoding
Access-Control-Allow-Credentials: true
X-XSS-Protection: 1; mode=block
X-Frame-Options: DENY
X-Download-Options: noopen
X-Content-Type-Options: nosniff
Content-Type: application/json; charset=utf-8
Content-Length: 84
ETag: W/"54-aWQn4djk3N5KQAOqWOqMF6qdqYc"
Date: Sat, 26 Oct 2019 02:19:10 GMT
        """
        filter = {
            "filter": {
                "where": {
                    "codigo": codigo,
                    "codigoRegiao": codigoRegiao
                }
            }
        }
        response = self.query('/api/grupos', params=filter)
        return None if response is None else Grupo(response)
