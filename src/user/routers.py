from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.auth.oauth2 import validate_token_from_headers, get_current_user
from src.user.schemas import User, UserCreate
from src.user import crud
from src.dependencies import get_async_session

router = APIRouter(tags=["users"])


@router.post("/users/", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(
        user: UserCreate,
        db: AsyncSession = Depends(get_async_session),
        user_id=Depends(validate_token_from_headers)
):
    """
    Create a new user and assign a role to them.

    The current user must be authenticated. The role assigned to the new user depends on the role of the current user.

    Args:
        user (UserCreate): The user to be created, obtained from the request body.
        db (AsyncSession): The database session.
        user_id (int): The ID of the current user, obtained from the authentication token.

    Returns:
        User: The created user.
    """
    try:
        current_user = await crud.get_user_by_id(db, id=user_id)
        return await crud.create_and_assign_role_to_user(db_session=db, user=user, current_user=current_user)
    except IntegrityError:
        raise HTTPException(status_code=400, detail="User with provided username or email already exists")


@router.get("/users/", response_model=list[User])
async def get_all_users(
        current_user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_async_session)
):
    """
    Retrieve all users.

    The current user must be authenticated.

    Args:
        db (AsyncSession): The database session.
        token (str): The authentication token of the current user.

    Returns:
        list[User]: A list of users.
    """
    return await crud.get_users_list(db_session=db)


@router.get("/users/{user_id}/", response_model=User)
async def user_detail(
        user_id: int,
        current_user: User = Depends(get_current_user),
        db_session: AsyncSession = Depends(get_async_session)):
    """
    Retrieve the details of a specific user.

    The current user must be authenticated.

    Args:
        user_id (int): The ID of the user to retrieve.
        db_session (AsyncSession): The database session.

    Returns:
        User: The details of the user.
    """
    db_user = await crud.get_user_detail(db_session=db_session, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    return db_user
