from tortoise import fields
from tortoise.models import Model


class User(Model):
    id = fields.IntField(pk=True)
    name = fields.TextField()
    email = fields.TextField()
    is_active = fields.BooleanField(default=True)

    def __str__(self):
        return self.name


class Todo(Model):
    id = fields.IntField(pk=True)
    title = fields.TextField()
    description = fields.BooleanField(default=True)
    owner = fields.ForeignKeyField("models.User", related_name="todos")
