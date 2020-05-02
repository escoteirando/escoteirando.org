from ..db.associado import Associado
from .base_dto import BaseDTO, date


class AssociadoDTO(Associado, BaseDTO):

    def __init__(self, from_dict: dict):
        self.codigo = self.get('codigo', int)
        self.cod_categoria = self.get('codigoCategoria', int)
        self.cod_equipe = self.get('codigoEquipe', int)
        self.cod_foto = self.get('codigoFoto', int)
        self.cod_ramo = self.get('codigoRamo', int)
        self.cod_ramo_adulto = self.get('codigoRamoAdulto', int)
        self.cod_segunda_categoria = self.get('codigoSegundaCategoria', int)
        self.cod_terceira_categoria = self.get('codigoTerceiraCategoria', int)
        self.dt_nascimento = self.get('dataNascimento', date)
        self.dt_validade = self.get('dataValidade', date)
        self.nome = self.get('nome', str)
        self.nome_abreviado = self.get('nome_abreviado', str)
        self.linha_formacao = self.get('linhaFormacao', str)
        self.sexo = self.get('sexo', str)
        self.username = self.get('username', int)
        self.numero_digito = self.get('numeroDigito', int)
