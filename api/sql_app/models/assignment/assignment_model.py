from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from ...database import Base


class Assignment(Base):
    __tablename__ = "assignments"

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    description = Column(String(150))
    homeworks = relationship("Homework", backref="assignment")
