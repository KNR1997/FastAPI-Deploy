from pydantic import BaseModel, Field


class BaseSubject(BaseModel):
    id: int
    name: str
    code: str


class SubjectCreate(BaseModel):
    name: str = Field(description="Maths")
    code: str = Field(description="MAT")


class SubjectUpdate(BaseModel):
    name: str = Field(description="maths")
    code: str = Field(description="MAT")


class SubjectOut(BaseModel):
    id: int
    name: str
    code: str

    model_config = {
        "from_attributes": True
    }
