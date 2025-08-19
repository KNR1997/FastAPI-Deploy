from app.models.subject import Subject
from typing import List, Optional, Tuple
from tortoise.expressions import Q


class SubjectRepository:
    async def paginated(
        self,
        page: int,
        page_size: int,
        search: Optional[Q] = None,
        order: Optional[List[str]] = None,
        prefetch: Optional[List[str]] = None
    ) -> Tuple[int, List[Subject]]:
        # Use default if no search
        query = Subject.filter(search) if search else Subject.all()
        if prefetch:
            query = query.prefetch_related(*prefetch)
        if order:
            query = query.order_by(*order)
        total = await query.count()
        records = await query.offset((page - 1) * page_size).limit(page_size)
        return total, list(records)

    async def create(self, **kwargs) -> Subject:
        subject = await Subject.create(**kwargs)
        return subject

    async def get(self, subject_id: int) -> Optional[Subject]:
        return await Subject.filter(id=subject_id).first()

    async def list(self) -> List[Subject]:
        return await Subject.all()

    async def update(self, subject_id: int, **kwargs) -> Optional[Subject]:
        subject = await self.get(subject_id)
        if not subject:
            return None
        for key, value in kwargs.items():
            setattr(subject, key, value)
        await subject.save()
        return subject

    async def delete(self, subject_id: int) -> bool:
        subject = await self.get(subject_id)
        if not subject:
            return False
        # await subject.delete(soft=False)
        return True

    async def exists(self, **kwards) -> bool:
        return await Subject.exists(**kwards)
