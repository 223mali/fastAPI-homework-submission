from enum import Enum
from typing import Optional
from datetime import datetime

from pydantic import BaseModel


class grade_enum(str, Enum):
    A = "A"
    B = "B"
    C = "C"
    D = "D"
    E = "E"
    F = "F"
    Incomplete = 'Incomplete'
    Ungraded = 'Ungraded'


class BaseModelEnum(BaseModel):
    class Config:
        use_enum_values = True


class Homework(BaseModelEnum):
    id: str
    assignment_id: str
    student_name: str
    submission_date: datetime
    grading_date: Optional[datetime]
    file_path: str
    finale_grade: str
    teacher_notes: str


class SubmitHomeWork(BaseModelEnum):
    assignment_id: str
    file_path: str
    filename: str


class GradeHomework(BaseModelEnum):
    finale_grade: grade_enum
    homework_id: int
    teacher_notes: Optional[str]


class UploadRes(BaseModel):
    file_path: Optional[str] = None
    message: str
    filename: Optional[str]
