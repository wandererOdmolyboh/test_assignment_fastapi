from fastapi import HTTPException
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.user.models import UserDB, SexEnum
from src.user.schemas import UserCreate, User


async def get_users_list(
        db_session: AsyncSession,
        sex: SexEnum | None = None
):
    query = select(UserDB)

    if sex is not None:
        query = query.where(UserDB.sex == sex)

    user_list = await db_session.execute(query)

    return user_list.scalars().all()


async def create_user(db_session: AsyncSession, user: UserCreate, current_user: User | None = None):
    query = insert(UserDB).values(
        username=user.username,
        email=user.email,
        role=user.role,
        created_by=None if current_user is None else current_user.id,
        sex=user.sex.value,
        password=user.password
    ).returning(UserDB.id)

    try:
        user_id = await db_session.execute(query)
        await db_session.commit()

        query = select(UserDB).where(UserDB.id == user_id.scalar_one())
        result = await db_session.execute(query)
        created_user = result.scalar_one()

        return created_user

    except Exception as e:
        await db_session.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


async def get_user_detail(db_session: AsyncSession, user_id: int):
    query = select(UserDB).where(UserDB.id == user_id)
    result = await db_session.execute(query)
    return result.scalar_one_or_none()


async def get_user_by_username(db_session: AsyncSession, username: str):
    query = select(UserDB).where(UserDB.username == username)
    result = await db_session.execute(query)
    return result.scalar_one_or_none()


async def get_user_by_id(db_session: AsyncSession, id: int):
    query = select(UserDB).where(UserDB.id == id)
    result = await db_session.execute(query)
    return result.scalar_one_or_none()
