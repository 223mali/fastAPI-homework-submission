import enum
from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey
import datetime
from ...database import Base


class grade_enum(enum.Enum):
    A = "A"
    B = "B"
    C = "C"
    D = "D"
    E = "E"
    F = "F"
    Incomplete = 'Incomplete'
    Ungraded = 'Ungraded'


class Homework(Base):
    __tablename__ = "homeworks"

    id = Column(Integer, primary_key=True)
    assignment_id = Column(Integer, ForeignKey('assignments.id'))
    homework_name = Column(String(50))
    user_id = Column(Integer, ForeignKey('users.id'))
    student_name = Column(String(50))
    submission_date = Column(DateTime, default=datetime.datetime.utcnow)
    grading_date = Column(DateTime)
    file_path = Column(String(50))
    finale_grade = Column(Enum(grade_enum))
    teacher_notes = Column(String(100))
