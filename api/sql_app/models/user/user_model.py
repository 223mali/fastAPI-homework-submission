import enum
from sqlalchemy import Column, Integer, String, DateTime, Enum
from sqlalchemy.orm import relationship
from sqlalchemy_utils import EmailType
import datetime
from ...database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)
    first_name = Column(String(50))
    last_name = Column(String(50))
    email = Column(EmailType, unique=True)
    hashed_password = Column(String(50))
    role = Column(String(10))
    homeworks = relationship("Homework", backref="user")
