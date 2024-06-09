from sqlalchemy import Column, Integer, String, Enum, ForeignKey
from enum import StrEnum

from sqlalchemy.orm import relationship

from src.database import Base
from src.message.models import DBMessage
from src.user.constant import ENUM_ADMIN, ENUM_MANAGER, ENUM_USER, ENUM_MALE, ENUM_FEMALE


class SexEnum(StrEnum):
    MALE = ENUM_MALE
    FEMALE = ENUM_FEMALE


class RoleEnum(StrEnum):
    ADMIN = ENUM_ADMIN
    MANGER = ENUM_MANAGER
    USER = ENUM_USER


class UserDB(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True, index=True)
    sex = Column(Enum(SexEnum), nullable=False)
    password = Column(String)
    role = Column(Enum(RoleEnum))
    created_by = Column(Integer, ForeignKey('users.id'), nullable=True)

    messages = relationship("DBMessage", back_populates="user")

