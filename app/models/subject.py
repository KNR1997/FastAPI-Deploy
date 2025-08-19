from tortoise import fields

from .base import BaseModel, TimestampMixin


class Subject(BaseModel):
    name = fields.CharField(max_length=20, unique=True, index=True)
    code = fields.CharField(max_length=20, unique=True, index=True)

    class Meta:
        table = "subject"
