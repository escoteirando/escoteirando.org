from datetime import date

from sqlalchemy import Date, Integer
from sqlalchemy_serializer import SerializerMixin

from escoteirando.ext.database import db

from ..dtos.base_dto import BaseDTO


class Associado(db.Model, SerializerMixin):

    id = db.Column(Integer, primary_key=True, autoincrement=True)
    codigo: int = db.Column(Integer, unique=True)
    cod_categoria: int = db.Column(Integer)
    cod_equipe: int = db.Column(Integer)
    cod_foto: int = db.Column(Integer)
    cod_ramo: int = db.Column(Integer)
    cod_ramo_adulto: int = db.Column(Integer)
    cod_segunda_categoria: int = db.Column(Integer)
    cod_terceira_categoria: int = db.Column(Integer)
    dt_nascimento: date = db.Column(Date)
    dt_validade: date = db.Column(Date)
    nome: str = db.Column(db.String(80))
    nome_abreviado: str = db.Column(db.String(80))
    linha_formacao: str = db.Column(db.String(30))
    sexo: str = db.Column(db.String(1))
    username: int = db.Column(Integer)
    numero_digito: int = db.Column(Integer)

    @staticmethod
    def from_dict(from_dict: dict):
        associado = Associado()
        dto = BaseDTO(from_dict)
        associado.codigo = dto.get('codigo', int)
        associado.cod_categoria = dto.get('codigoCategoria', int)
        associado.cod_equipe = dto.get('codigoEquipe', int)
        associado.cod_foto = dto.get('codigoFoto', int)
        associado.cod_ramo = dto.get('codigoRamo', int)
        associado.cod_ramo_adulto = dto.get('codigoRamoAdulto', int)
        associado.cod_segunda_categoria = dto.get(
            'codigoSegundaCategoria', int)
        associado.cod_terceira_categoria = dto.get(
            'codigoTerceiraCategoria', int)
        associado.dt_nascimento = dto.get('dataNascimento', date)
        associado.dt_validade = dto.get('dataValidade', date)
        associado.nome = dto.get('nome', str)
        associado.nome_abreviado = dto.get('nome_abreviado', str)
        associado.linha_formacao = dto.get('linhaFormacao', str)
        associado.sexo = dto.get('sexo', str)
        associado.username = dto.get('username', int)
        associado.numero_digito = dto.get('numeroDigito', int)
        return associado
