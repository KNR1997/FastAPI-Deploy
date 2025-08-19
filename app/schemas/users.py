from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field


class BaseUser(BaseModel):
    id: int
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    last_login: Optional[datetime]
    roles: Optional[list] = []


class UserCreate(BaseModel):
    full_name: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    name_with_initials: Optional[str] = None
    username: str = Field(description="admin")
    email: EmailStr = Field(description="admin@qq.com")
    password: str = Field(description="123456")
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    role_ids: Optional[List[int]] = []
    dept_id: Optional[int] = Field(0, description="部门ID")

    def create_dict(self):
        return self.model_dump(exclude_unset=True, exclude={"role_ids"})


class UserUpdate(BaseModel):
    # id: int
    full_name: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    name_with_initials: Optional[str] = None
    nic: Optional[str] = None
    username: str
    email: EmailStr
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    role_ids: Optional[List[int]] = []
    dept_id: Optional[int] = 0


class UpdatePassword(BaseModel):
    old_password: str = Field(description="旧密码")
    new_password: str = Field(description="新密码")
    

class UserOut(BaseModel):
    id: int
    email: EmailStr
    username: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None

    model_config = {
        "from_attributes": True
    }
