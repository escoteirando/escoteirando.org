from mongoengine import Document, IntField


class Equipe(Document):
    codigo_equipe = IntField()
    # TODO: Itentificar modelagem da equipe

    def __dict__(self):
        return {
            "codigo_equipe": self.codigo_equipe
        }
