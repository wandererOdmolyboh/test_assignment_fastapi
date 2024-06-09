from pydantic import BaseModel
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
