from flask_mongoengine import MongoEngine
from mongoengine import BinaryField, DateTimeField, StringField
from datetime import datetime


class CachedItemModel(MongoEngine().Document):
    creation_time = DateTimeField(default=datetime.now(), required=True)
    content = BinaryField()
    url = StringField()
