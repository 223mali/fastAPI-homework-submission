from typing import Optional

from pydantic import BaseModel


class BaseModelORM(BaseModel):
    class Config:
        orm_mode = True


class CreateAssignment(BaseModelORM):
    name: str
    description: str


class ReturnedAssignment(CreateAssignment):
    id: str
