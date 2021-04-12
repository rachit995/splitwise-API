import datetime
from mongoengine import connect, Document, StringField, ReferenceField, DateTimeField, MapField, ListField
from mongoengine.fields import DictField, IntField
from application.config import DevelopmentConfig
from application.models.group import Group
import json

config = DevelopmentConfig()

connect(host=config.MONGO_URI)


class Expense(Document):
    title = StringField(required=True)
    amount = IntField(required=True)
    group = ReferenceField(Group)
    spender = StringField(required=True)
    splits = StringField(required=True)
    created_at = DateTimeField(default=datetime.datetime.now)

    def deserialize(self):
        return {
            "id": str(self.id),
            "title": self.title,
            "spender": json.loads(self.spender),
            "splits": json.loads(self.splits),
            "amount": self.amount,
            "group": self.group.deserialize(),
        }
