from typing import List, Tuple
from tortoise.expressions import Q

# from app.core.exceptions import ValidationException
from app.models.subject import Subject
from app.repositories.subject_repository import SubjectRepository
from app.schemas.subject import SubjectCreate, SubjectUpdate


class SubjectService:
    def __init__(self, repository: SubjectRepository):
        self.repository = repository

    async def paginated_subjects(
        self, page: int, page_size: int, search: Q = Q(), order: list = []
    ) -> Tuple[int, List[Subject]]:
        return await self.repository.paginated(page, page_size, search, order)

    async def list_subjects(self) -> list[Subject]:
        return await self.repository.list()

    async def get_subject(self, subject_id: int) -> Subject | None:
        return await self.repository.get(subject_id)

    async def create_subject(self, subject_data: SubjectCreate) -> Subject:
        exists = await self.repository.exists(code=subject_data.code)
        # if exists:
        #     raise ValidationException(
        #         validation={"code": ["Subject already exists with this code."]})
        return await self.repository.create(**subject_data.model_dump())

    async def update_subject(self, subject_id: int, subject_data: SubjectUpdate) -> Subject | None:
        subject = await self.get_subject(subject_id=subject_id)
        if subject and subject.code != subject_data.code:
            exists = self.repository.exists(code=subject_data.code)
            # if exists:
            #     raise ValidationException(
            #         validation={"code": ["Subject already exists with this code."]})
        return await self.repository.update(subject_id, **subject_data.model_dump(exclude_unset=True))

    async def delete_subject(self, subject_id: int) -> bool:
        return await self.repository.delete(subject_id)