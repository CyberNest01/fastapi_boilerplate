from tortoise.models import Model
from tortoise import fields


class TimestampMixin:
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)


class BaseModel(Model):
    id = fields.IntField(primary_key=True)

    class Meta:
        abstract = True
