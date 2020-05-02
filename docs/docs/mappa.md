# mAppa Login

API de acesso aos dados do escotista e da seção

## Login: POST /api/escotistas/login

``` json
{
    "type": "LOGIN_REQUEST",
    "username": "username",
    "password": "password"
}
```

### Response
``` json
{
    "id": "904QVxCGR0mLG6uDqWt7EOZLZZyfbaBRatKnoMefohwfkpPjc5jeuyUNAWED5t7H",
    "ttl": 1209600,
    "created": "2019-10-26T02:19:09.146Z",
    "userId": 50442
}
```

* id = Chave de autorização utilizada em todas as requisições. Deve ser enviada como um header:

``` json
{
    "authorization":"904QVxCGR0mLG6uDqWt7EOZLZZyfbaBRatKnoMefohwfkpPjc5jeuyUNAWED5t7H"
}
```

* ttl = Time-to-live, tempo em segundos da validade da chave de autorização
* created = Data de criação da autorização
* userId = código utilizado para consultar o escotista

## Escotista: GET /api/escotistas/{userId}

### Response

``` json
{
    "codigo":50442,
    "codigoAssociado":850829,
    "username":"Guionardo",
    "nomeCompleto":"GuionardoFurlan",
    "ativo":"S",
    "codigoGrupo":32,
    "codigoRegiao":"SC",
    "codigoFoto":null
}
```

## Associado: GET /api/associados/{codigoAssociado}

### Response

``` json
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
```

## Grupo: GET /api/grupos?filter={"where":{"codigo":_codigoGrupo_,"codigoRegiao":"_codigoRegiao_"}}

### Response

``` json
[{
    "codigo":32,
    "codigoRegiao":"SC",
    "nome":"LEÕES DE BLUMENAU",
    "codigoModalidade":1
}]
```

## Seção: GET /api/escotistas/{userId}/secoes

### Response

``` json
[{
    "codigo": 1424,
    "nome": "ALCATÉIA 1",
    "codigoTipoSecao": 1,
    "codigoGrupo": 32,
    "codigoRegiao": "SC"
}]
```

## Associados: GET / api/escotistas/{userId}/secoes/{codigoSecao}/equipes?filter={"include":"associados"}
