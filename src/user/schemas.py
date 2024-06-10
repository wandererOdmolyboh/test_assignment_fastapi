from pydantic import BaseModel, field_validator
from pydantic_core.core_schema import ValidationInfo

from src.auth.utils import hash_password
from src.user.models import SexEnum, RoleEnum


class UserBase(BaseModel):
    """
    A Pydantic model that defines the basic attributes of a user. This model includes fields for the user's username,
    email, sex, role, and the ID of the user who created this user.

    Args:
        username (str): The username of the user.
        email (str): The email address of the user.
        sex (SexEnum): The sex of the user. This must be one of the values defined in the SexEnum class.
        role (RoleEnum): The role of the user. This must be one of the values defined in the RoleEnum class.
        created_by (int | None): The ID of the user who created this user. This can be None if the user was not
        created by another user.
    """
    username: str
    email: str
    sex: SexEnum
    role: RoleEnum
    created_by: int | None


class UserCreate(UserBase):
    """
    A Pydantic model that defines the data required to create a new user. This model inherits all fields from UserBase,
    and adds a field for the user's password.

    Args:
        password (str): The password of the user.
    """
    password: str

    @field_validator('password')
    def hash_password(cls, password):
        return hash_password(password)

    @field_validator('role')
    def set_role(cls, role, info: ValidationInfo):
        if 'current_user' not in info.data or info.data['current_user'] is None:
            return RoleEnum.USER
        current_user = info.data['current_user']
        if current_user.role == RoleEnum.ADMIN:
            return role
        return RoleEnum.USER

    @field_validator('created_by')
    def set_created_by(cls, created_by, info: ValidationInfo):

        if 'current_user' in info.data:
            current_user = info.data['current_user']
            return None if current_user is None else current_user.id
        return created_by

    class ConfigDict:
        """
        A nested class for Pydantic model configuration. The 'from_attributes' attribute is set to True, which means
        that attributes of the model instance will be used to populate the dictionary when the model is converted to a
        dictionary using the 'dict()' function.
        """
        from_attributes = True


class User(UserBase):
    """
    A Pydantic model representing a user. This model inherits all fields from UserBase and adds an 'id' field.

    Args:
        id (int): The user's ID.
    """
    id: int

    class ConfigDict:
        """
        A nested class for Pydantic model configuration. The 'from_attributes' attribute is set to True, which means
        that attributes of the model instance will be used to populate the dictionary when the model is converted to a
        dictionary using the 'dict()' function.
        """
        from_attributes = True
