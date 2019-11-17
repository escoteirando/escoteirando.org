from models.mappa.associado_response import Associado

from .request import query


def associado(codigoAssociado):
    response = query(f'/api/associados/{codigoAssociado}')
    if response is None:
        return None
    return Associado(response)

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
