from .request import query
from domain.models.mappa.escotista_response import Escotista


def escotista(userId) -> Escotista:
    response = query(f'/api/escotistas/{userId}')
    if response is None:
        return None

    return Escotista(response.content)


'''
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
'''
