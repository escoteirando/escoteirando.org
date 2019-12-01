from domain.models.mappa.especialidade_response import Especialidade
from domain.models.mappa.progressao_response import Progressao

from .mappa_base_service import MappaService


class MappaCadastrosService(MappaService):

    def get_especialidades(self):
        filter = {
            "filter[include]": "itens"
        }
        response = self.query('/api/especialidades', filter)

        if isinstance(response, list):
            for especialidade in response:
                especialidade = Especialidade(especialidade)

        return response

    def get_progressoes(self):
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
        response = self.query('/api/progressao-atividades', filter)
        if isinstance(response, list):
            for progressao in response:
                progressao = Progressao(progressao)

        return response
