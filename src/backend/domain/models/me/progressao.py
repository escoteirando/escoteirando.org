from mongoengine import Document, IntField, StringField


class Progressao(Document):
    codigo = IntField(required=True)
    descricao = StringField(required=True)
    codigoUeb = StringField(required=True, primary_key=True)
    ordenacao = IntField(required=True)
    codigoCaminho = IntField()
    codigoDesenvolvimento = IntField()
    codigoCompetencia = IntField()
    segmento = StringField()


'''
     {
        "codigo": 1,
        "descricao": "Ouvir o episódio \"Irmãos de Mowgli\" do Livro da Selva.",
        "codigoUeb": "S2",
        "ordenacao": 2,
        "codigoCaminho": 1,
        "codigoDesenvolvimento": 23,
        "numeroGrupo": null,
        "codigoRegiao": null,
        "codigoCompetencia": 38,
        "segmento": "PROMESSA_ESCOTEIRA_LOBINHO"
    }
'''
