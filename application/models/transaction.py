
from application.models.expense import Expense
import datetime
from mongoengine import connect, Document, StringField, ReferenceField, DateTimeField
from application.models.user import User
from mongoengine.fields import IntField
from application.config import DevelopmentConfig

config = DevelopmentConfig()

connect(host=config.MONGO_URI)


class Transaction(Document):
    amount = IntField(required=True)
    payee = ReferenceField(User)
    payer = ReferenceField(User)
    expense = ReferenceField(Expense)
    created_at = DateTimeField(default=datetime.datetime.now)

    def deserialize(self):
        return {
            "id": str(self.id),
            "amount": self.amount,
            "payee": self.payee.deserialize(),
            "payer": self.payer.deserialize(),
        }
