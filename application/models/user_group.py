
import datetime
from application.models.group import Group
from application.models.user import User
from mongoengine import connect, Document, StringField, ReferenceField, DateTimeField
from application.config import DevelopmentConfig

config = DevelopmentConfig()

connect(host=config.MONGO_URI)


class UserGroup(Document):
    user = ReferenceField(User)
    group = ReferenceField(Group)
    created_at = DateTimeField(default=datetime.datetime.now)
