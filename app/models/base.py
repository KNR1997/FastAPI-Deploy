import asyncio
from datetime import datetime

from tortoise import fields, models

from app.settings import settings


class BaseModel(models.Model):
    id = fields.BigIntField(pk=True, index=True)

    async def to_dict(self, m2m: bool = False, exclude_fields: list[str] | None = None):
        if exclude_fields is None:
            exclude_fields = []

        d = {}
        for field in self._meta.db_fields:
            if field not in exclude_fields:
                value = getattr(self, field)
                if isinstance(value, datetime):
                    value = value.strftime(settings.DATETIME_FORMAT)
                d[field] = value

        if m2m:
            tasks = [
                self.__fetch_m2m_field(field, exclude_fields)
                for field in self._meta.m2m_fields
                if field not in exclude_fields
            ]
            results = await asyncio.gather(*tasks)
            for field, values in results:
                d[field] = values

        return d

    async def __fetch_m2m_field(self, field, exclude_fields):
        values = await getattr(self, field).all().values()
        formatted_values = []

        for value in values:
            formatted_value = {}
            for k, v in value.items():
                if k not in exclude_fields:
                    if isinstance(v, datetime):
                        formatted_value[k] = v.strftime(settings.DATETIME_FORMAT)
                    else:
                        formatted_value[k] = v
            formatted_values.append(formatted_value)

        return field, formatted_values

    class Meta:
        abstract = True


class UUIDModel:
    uuid = fields.UUIDField(unique=True, pk=False, index=True)


class TimestampMixin:
    created_at = fields.DatetimeField(auto_now_add=True, index=True)
    updated_at = fields.DatetimeField(auto_now=True, index=True)


# class UserAuditMixin:
#     # pass
#     created_by: fields.ForeignKeyNullableRelation["User"] = fields.ForeignKeyField(
#         "models.User", null=True, related_name=None
#     )
#     updated_by: fields.ForeignKeyNullableRelation["User"] = fields.ForeignKeyField(
#         "models.User", null=True, related_name=None
#     )

# class UserAuditMixin:
#     created_at = fields.DatetimeField(auto_now_add=True)
#     created_by = fields.ForeignKeyField(
#         "models.User", 
#         related_name=False,
#         null=True
#     )
#     updated_at = fields.DatetimeField(auto_now=True)
#     updated_by = fields.ForeignKeyField(
#         "models.User", 
#         related_name=False,
#         null=True
#     )

# class Timestamp:
#     created_at = fields.DatetimeField(auto_now_add=True, index=True)
#     updated_at = fields.DatetimeField(auto_now=True, index=True)


# class SoftDeleteMixin:
#     deleted_at = fields.DatetimeField(null=True)

#     async def soft_delete(self, user=None):
#         self.deleted_at = datetime.utcnow()
#         if user:
#             self.updated_by = user
#         await self.save()


# class AuditModel(models.Model, TimestampMixin, UserAuditMixin, SoftDeleteMixin):
#     id = fields.UUIDField(unique=True, pk=True, index=True)

#     class Meta:
#         abstract = True

#     async def save_with_user(self, user=None, *args, **kwargs):
#         if self._saved_in_db:
#             self.updated_by = user
#         else:
#             self.created_by = user
#         await self.save(*args, **kwargs)


class Timestamp(models.Model):
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    
    class Meta:
        abstract = True


class UserAudit(models.Model):
    created_by = fields.ForeignKeyField(
        "models.User", 
        related_name=False,
        null=True
    )
    updated_by = fields.ForeignKeyField(
        "models.User", 
        related_name=False,
        null=True
    )
    
    class Meta:
        abstract = True


class SoftDelete(models.Model):
    deleted_at = fields.DatetimeField(null=True)

    async def soft_delete(self, user=None):
        self.deleted_at = datetime.utcnow()
        if user:
            self.updated_by = user
        await self.save()


class AuditModel(models.Model):
    id = fields.BigIntField(pk=True, index=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    deleted_at = fields.DatetimeField(null=True)
    created_by = fields.ForeignKeyField(
        "models.User", 
        related_name=False,
        null=True
    )
    updated_by = fields.ForeignKeyField(
        "models.User", 
        related_name=False,
        null=True
    )

    # Soft delete methods
    async def soft_delete(self, user=None):
        self.deleted_at = datetime.now()
        if user:
            self.updated_by = user
        await self.save()

    async def to_dict(self, m2m: bool = False, exclude_fields: list[str] | None = None):
        if exclude_fields is None:
            exclude_fields = []

        d = {}
        for field in self._meta.db_fields:
            if field not in exclude_fields:
                value = getattr(self, field)
                if isinstance(value, datetime):
                    value = value.strftime(settings.DATETIME_FORMAT)
                d[field] = value

        if m2m:
            tasks = [
                self.__fetch_m2m_field(field, exclude_fields)
                for field in self._meta.m2m_fields
                if field not in exclude_fields
            ]
            results = await asyncio.gather(*tasks)
            for field, values in results:
                d[field] = values

        return d

    async def __fetch_m2m_field(self, field, exclude_fields):
        values = await getattr(self, field).all().values()
        formatted_values = []

        for value in values:
            formatted_value = {}
            for k, v in value.items():
                if k not in exclude_fields:
                    if isinstance(v, datetime):
                        formatted_value[k] = v.strftime(settings.DATETIME_FORMAT)
                    else:
                        formatted_value[k] = v
            formatted_values.append(formatted_value)

        return field, formatted_values

    class Meta:
        abstract = True
