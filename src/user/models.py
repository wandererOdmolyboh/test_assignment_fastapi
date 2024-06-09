from sqlalchemy import Column, Integer, String, Enum, ForeignKey
from enum import StrEnum

from sqlalchemy.orm import relationship

from src.database import Base


class SexEnum(StrEnum):
    MALE = "Male"
    FEMALE = "Female"


class RoleEnum(StrEnum):
    ADMIN = "admin"
    MANGER = "manager"
    USER = "user"


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

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "sex": self.sex,
            "password": self.password,
            "role": self.role,
            "created_by": self.created_by,
        }