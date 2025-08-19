from tortoise import fields

from .base import BaseModel, TimestampMixin
from .enums import MethodType


class User(BaseModel, TimestampMixin):
    full_name = fields.TextField(null=True)
    first_name = fields.TextField(null=True, description="First Name")
    last_name = fields.TextField(null=True, description="Last Name")
    name_with_initials = fields.TextField(null=True)
    username = fields.CharField(max_length=20, unique=True, index=True)
    alias = fields.CharField(max_length=30, null=True, index=True)
    email = fields.CharField(max_length=191, unique=True, index=True)
    phone = fields.CharField(max_length=20, null=True, index=True)
    nic = fields.TextField(max_length=30, null=True, description="NIC number")
    password = fields.TextField(null=True, description="Password")
    is_active = fields.BooleanField(default=True, index=True)
    is_superuser = fields.BooleanField(default=False, index=True)
    last_login = fields.DatetimeField(null=True,  index=True)

    class Meta:
        table = "user"
