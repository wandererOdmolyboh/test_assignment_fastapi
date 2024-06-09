from sqlalchemy.ext.asyncio import AsyncSession

from src.auth import hash_password
from src.user import crud as user_crud
from src.user.models import SexEnum, RoleEnum
from src.user.schemas import UserCreate


def test_set_user():
    return [
        {
            "username": "admin",
            "email": "admin@test.com",
            "password": hash_password("admin"),
            "sex": SexEnum.MALE,
            "role": RoleEnum.ADMIN,
            "created_by": None
        },
        {
            "username": "user",
            "email": "user@test.com",
            "password": hash_password("user"),
            "sex": SexEnum.FEMALE,
            "role": RoleEnum.USER,
            "created_by": None
        },
        {
            "username": "manager",
            "email": "manager@test.com",
            "password": hash_password("manager"),
            "sex": SexEnum.FEMALE,
            "role": RoleEnum.MANGER,
            "created_by": None
        }
    ]


async def create_test_users(db: AsyncSession):
    test_users = [UserCreate(**user) for user in test_set_user()]

    for user in test_users:
        await user_crud.create_user(db, user=user)
