from fastapi import HTTPException
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.user.models import UserDB, SexEnum, RoleEnum
from src.user.schemas import UserCreate, User

from src.auth.hash_password import hash_password


async def get_users_list(
        db_session: AsyncSession,
        sex: SexEnum | None = None
):
    query = select(UserDB)

    if sex is not None:
        query = query.where(UserDB.sex == sex)

    user_list = await db_session.execute(query)

    return user_list.scalars().all()


async def create_and_assign_role_to_user(db_session: AsyncSession, user: UserCreate, current_user: User | None = None):
    user.password = hash_password(user.password)

    if current_user is None or current_user.role in (RoleEnum.MANGER, RoleEnum.USER):
        role = RoleEnum.USER
    else:
        role = user.role
    user.role = role
    user.created_by = None if current_user is None else current_user.id
    return await create_user(db_session, user)


async def create_user(db_session: AsyncSession, user: UserCreate):
    query = insert(UserDB).values(
        username=user.username,
        email=user.email,
        role=user.role,
        created_by=user.created_by,
        sex=user.sex.value,
        password=user.password
    ).returning(UserDB.id)

    try:
        # TODO
        result = await db_session.execute(query)
        user_id = result.scalar_one()
        await db_session.commit()
        response = {**user.model_dump(), "id": user_id}
        return response
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
