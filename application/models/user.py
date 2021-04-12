import datetime
from mongoengine import connect, Document, StringField, ReferenceField, DateTimeField
from application.config import DevelopmentConfig

config = DevelopmentConfig()

connect(host=config.MONGO_URI)


class User(Document):
    name = StringField(required=True)
    created_at = DateTimeField(default=datetime.datetime.now)

    def deserialize(self):
        return {
            "id": str(self.id),
            "name": self.name,
        }
