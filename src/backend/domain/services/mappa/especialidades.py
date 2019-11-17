from domain.models.mappa.especialidade_response import Especialidade

from .request import query


def especialidades():
    filter = {
        "filter[include]": "itens"
    }
    response = query('/api/especialidades', filter)

    if isinstance(response, list):
        for especialidade in response:
            especialidade = Especialidade(especialidade)

    return response
