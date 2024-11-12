from tortoise import fields

from app.models import BaseModel, TimestampMixin


class User(BaseModel, TimestampMixin):
    username = fields.CharField(max_length=50)

