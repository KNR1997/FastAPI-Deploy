from typing import Any, Dict, Generic, List, Optional, NewType, Tuple, Type, TypeVar, Union
from datetime import datetime

from pydantic import BaseModel
from tortoise.expressions import Q
from tortoise.models import Model

from app.models import User

Total = NewType("Total", int)
ModelType = TypeVar("ModelType", bound=Model)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get(self, id: int) -> ModelType:
        return await self.model.get(id=id)

    async def list(
            self, 
            page: int, 
            page_size: int, 
            search: Q = Q(), 
            order: list = []
    ) -> Tuple[Total, List[ModelType]]:
        # Check if 'deleted_at' is a field on the model
        if 'deleted_at' in self.model._meta.fields_map:
            search &= Q(deleted_at__isnull=True)

        query = self.model.filter(search)
        return (
            await query.count(),
            await query
                .offset((page - 1) * page_size)
                .limit(page_size)
                .order_by(*order),
        )

    async def create(
            self, 
            obj_in: CreateSchemaType,
            current_user: Optional[User] = None
    ) -> ModelType:
        obj_dict = obj_in if isinstance(obj_in, dict) else obj_in.model_dump()

        # Handle audit fields if they exist
        if hasattr(self.model, "created_by"):
            obj_dict["created_by"] = current_user
        if hasattr(self.model, "updated_by"):
            obj_dict["updated_by"] = current_user

        obj = self.model(**obj_dict)
        await obj.save()
        return obj

    async def update(
            self, id: int, 
            obj_in: Union[UpdateSchemaType, 
            Dict[str, Any]],
            current_user: Optional[User] = None
    ) -> ModelType:
        if isinstance(obj_in, Dict):
            obj_dict = obj_in
        else:
            obj_dict = obj_in.model_dump(exclude_unset=True, exclude={"id"})

        # Handle audit fields if they exist
        if hasattr(self.model, "updated_by"):
            obj_dict["updated_by"] = current_user

        obj = await self.get(id=id)
        obj = obj.update_from_dict(obj_dict)
        await obj.save()
        return obj

    async def soft_delete(
            self,
            id: int, 
            user: Optional[User] = None
    ) -> ModelType:
        obj = await self.get(id=id)
        if hasattr(obj, "deleted_at"):
            obj.deleted_at = datetime.now()
        if hasattr(obj, "deleted_by"):
            obj.deleted_by = user
        await obj.save()
        return obj

    async def remove(self, id: int) -> None:
        obj = await self.get(id=id)
        await obj.delete()
