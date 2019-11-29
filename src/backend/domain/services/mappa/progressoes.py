from domain.models.mappa.progressao_response import Progressao

from .request import query


def progressoes():
    # TODO: Verificar o parâmetro de codigoCaminho para outras seções além de lobinho
    filter = {
        "filter": {
            "where": {
                "numeroGrupo": None,
                "codigoRegiao": None,
                "codigoCaminho": {
                    "in": [1, 2, 3, 4, 5, 6, 11, 12, 15, 16]
                }
            }
        }
    }
    response = query('/api/progressao-atividades', filter)
    if isinstance(response, list):
        for progressao in response:
            progressao = Progressao(progressao)

    return response
