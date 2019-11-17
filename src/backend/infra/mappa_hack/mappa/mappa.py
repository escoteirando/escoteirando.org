import gzip
import json
import os
import pprint
import urllib.parse
from datetime import datetime, timedelta
from io import BytesIO, StringIO
from time import sleep
from .services import Cache, get

import requests
from progress.spinner import PixelSpinner

from .associado import Associado
from .cache import Cache
from .escotista import Escotista
from .grupo import Grupo
from .sessao import Sessao
from .subsessao import Subsessao


class Mappa:

    def __init__(self):
        self._url = "http://mappa.escoteiros.org.br"
        self.cache = Cache()
        self.authorization = None
        self.userId = None
        self.escotista = None
        self.associado = None
        self.grupo = None
        self.especialidades = None
        self.sessao = None
        self.subsessoes=None
        self.equipe = None
        self.error = None
        self.last_get = None
        self.last_call = "INIT"
        self.file_auth = os.path.join(os.path.dirname(__file__), ".auth")

    def get_auth(self, username):
        if not os.path.isfile(self.file_auth):
            return False
        with open(self.file_auth, 'r') as f:
            if f.readable():
                auths = json.loads(f.read())
            else:
                auths = {}
        if username in auths:
            auth = auths[username]
            dvalid = datetime.strptime(auth['valid'], "%Y-%m-%d %H:%M:%S")
            if dvalid > datetime.now():
                self.authorization = auth['authentication']
                self.userId = auth['userId']
                if "escotista" in auth:
                    self.escotista = Escotista(auth["escotista"])
                print("Get auth from cache")
                return True

        return False

    def set_auth(self, username, login_response, escotista=None):
        auths = {}
        f = "%Y-%m-%dT%H:%M:%S"
        valid_date = datetime.strptime(login_response['created'][0:19], f)

        auth_obj = {
            "authentication": login_response["id"],
            "userId": login_response["userId"],
            "created": login_response["created"],
            "valid": str(valid_date + timedelta(seconds=login_response['ttl'])),
            "escotista": escotista
        }
        if not os.path.isfile(self.file_auth):
            with open(self.file_auth, 'w') as f:
                f.write("{}")

        with open(self.file_auth, 'r+') as f:
            if f.readable():
                auths = json.loads(f.read())
            else:
                auths = {}

            auths[username] = auth_obj
            f.seek(0, 0)
            f.truncate()
            f.write(json.dumps(auths))

    def __str__(self):
        return pprint.pformat(self.__dict__)

    def get(self, url, params=None, description=None, gzipped=False):
        self.last_get = None
        self.error = None
        if not description:
            description = url
        if not self.authorization:
            self.error = 'LOGIN ERROR BEFORE '+description
            return False

        _headers = {
            "authorization": self.authorization,
            "User-Agent": "okhttp/3.4.1"
        }
        if (gzipped):
            _headers["Accept-Encoding"] = "gzip"

        cache = self.cache.readCache(url, _headers)
        if cache:
            self.last_get = json.loads(cache)
            return True

        count = 0
        success = False
        exceptions = []
        while count < 5 and not success:
            count += 1
            try:
                print(url)
                ret = requests.get(
                    self._url+url, json=params, headers=_headers)
                if ret.status_code == 200:
                    content = ret.content.decode("utf-8")
                    self.last_get = json.loads(content)
                    self.cache.writeCache(url, content, _headers)
                    success = True
                else:
                    self.error = json.loads(ret.text)
            except Exception as e:
                if str(e) not in exceptions:
                    exceptions.append(str(e))
                if count == 1:
                    print("Retrying .", end="")
                elif count < 5:
                    print(".", end="")
                else:
                    print(". timeout")
                    print("Exceptions:"+pprint.pformat(exceptions))

                if count < 5:
                    sleep(1)

        if len(exceptions) > 0:
            self.error = exceptions
        return success

    def login(self, username, password):
        self.last_call = f"login({username},{password})"
        if self.get_auth(username):
            return True
        url = self._url + "/api/escotistas/login"
        body = {
            "type": "LOGIN_REQUEST",
            "username": username,
            "password": password
        }
        try:
            ret = requests.post(url, json=body, headers={
                "User-Agent": "okhttp/3.4.1"})

            if ret.status_code == 200:
                login_response = json.loads(ret.content)
                self.userId = login_response['userId']
                self.authorization = login_response['id']

                if self.get_escotista():
                    self.set_auth(username, login_response, self.escotista)
                else:
                    self.set_auth(username, login_response)

                return True
        except Exception as e:
            self.error = str(e)

        return False

    def get_escotista(self):
        self.last_call = f"get_escotista()"
        if self.escotista:
            print("get_escotista from cache:")
            pprint.pprint(self.escotista)
            return True

        if self.get("/api/escotistas/"+str(self.userId), description="Escotista"):
            self.escotista = Escotista(self.last_get)
            print("get_escotista:")
            pprint.pprint(self.escotista)
            # {"codigo":50442,"codigoAssociado":850829,"username":"Guionardo","nomeCompleto":"GuionardoFurlan","ativo":"S","codigoGrupo":32,"codigoRegiao":"SC","codigoFoto":null}
            return True

        return False

    def get_especialidades(self):
        self.last_call = "get_especialidades()"
        if self.get("/api/setup/especialidade-quantidades", gzipped=True, description="Especialidades"):
            self.especialidades_quant = self.last_get            
    
        self.last_get = "get_especialidades()"
        if self.get('/api/especialidades?filter[include]=itens',gzipped=True):
            self.especialidades = self.last_get
            
        return False

    def get_filter(self, filter):
        cfilter = urllib.parse.quote(json.dumps(filter))
        return cfilter

    def get_grupo(self):
        self.last_call = "get_grupo()"
        cfilter = self.get_filter({
            "where": {
                "codigo": self.escotista.codigoGrupo,
                "codigoRegiao": self.escotista.codigoRegiao
            }
        })
        if self.get(f"/api/grupos?filter={cfilter}"):
            self.grupo = Grupo(self.last_get[0])
            return True

        return False

        # /api/grupos?filter={%22where%22:%20{%22codigo%22:%2032,%20%22codigoRegiao%22:%20%22SC%22}}
        #[{"codigo":32,"codigoRegiao":"SC","nome":"LEÕES DE BLUMENAU","codigoModalidade":1}]

    def get_associado(self):
        self.last_call = "get_associado()"
        if self.get(f"/api/associados/{self.escotista.codigoAssociado}"):
            self.associado = Associado(self.last_get)
            return True

        return False
        # /api/associados/850829

    def get_sessoes(self):
        self.last_call = "get_sessoes()"
        if self.get(f"/api/escotistas/{self.userId}/secoes"):
            self.sessao = Sessao(self.last_get[0])
            return True

        return False

        # /api/escotistas/50442/secoes
        #[{"codigo":1424,"nome":"ALCATÉIA 1 ","codigoTipoSecao":1,"codigoGrupo":32,"codigoRegiao":"SC"}]

    def get_equipe(self):
        self.last_call = "get_equipe()"
        cfilter = self.get_filter({"include": "associados"})
        if self.get(f'/api/escotistas/{self.userId}/secoes/{self.sessao.codigo}/equipes?filter={cfilter}'):
            self.subsessoes=[]
            for subsessao in self.last_get:
                css = Subsessao(subsessao)
                if css.ok:
                    self.subsessoes.append(css)

            self.equipe = self.last_get
            return True

        return False
        # GET /api/escotistas/50442/secoes/1424/equipes?filter={%22include%22:%20%22associados%22}

    def get_marcacoes(self):
        self.last_get = "get_marcacoes()"
        if self.get(f'/api/marcacoesAdultos/updates?dataHoraUltimaAtualizacao=1970-01-01T00:00:00.000Z&codigoEscotista={self.userId}'):
            self.marcacoes = self.last_get
        # /api/marcacoesAdultos/updates?dataHoraUltimaAtualizacao=1970-01-01T00:00:00.000Z&codigoEscotista=5044

