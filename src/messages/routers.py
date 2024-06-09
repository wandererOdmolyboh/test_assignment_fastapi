from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.utils.token import TokenValidationError
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.messages import crud, schemas
from src.messages.schemas import Message
from src.auth.oauth2 import get_current_active_user
from src.dependencies import get_async_session
from src.user.models import RoleEnum
from src.user.schemas import User

router = APIRouter(tags=["messages"])


@router.get("/messages/", response_model=list[Message])
async def get_messages(current_user: User = Depends(get_current_active_user),
                       db: AsyncSession = Depends(get_async_session)):
    """
    Retrieve all messages based on the role of the current user.

    If the current user is an admin, all messages are returned.
    If the current user is a manager, only messages sent by this manager and users created by this manager are returned.
    If the current user is a user, only messages sent by this user are returned.

    Args:
        current_user (User): The current user, obtained from the authentication token.
        db (AsyncSession): The database session.

    Returns:
        list[Message]: A list of messages.
    """

    if current_user.role == RoleEnum.ADMIN:
        messages = await crud.get_all_messages(db)
    elif current_user.role == RoleEnum.MANGER:
        messages = await crud.get_manager_all_messages(db, current_user.id)

    elif current_user.role == RoleEnum.USER:
        messages = await crud.get_user_all_messages(db, current_user.id)
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="You do not have permission to perform this action")

    return messages


@router.post("/message/", response_model=Message, status_code=status.HTTP_201_CREATED)
async def create_message(
        message: schemas.MessageCreate,
        current_user: User = Depends(get_current_active_user),
        db: AsyncSession = Depends(get_async_session)
):
    """
    Create a new message and send it to a specified chat in Telegram.

    The current user must be authenticated. After the message is created, it is sent to the specified chat in Telegram.

    Args:
        message (schemas.MessageCreate): The message to be created, obtained from the request body.
        current_user (User): The current user, obtained from the authentication token.
        db (AsyncSession): The database session.

    Returns:
        Message: The created message.
    """
    created_message = await crud.create_message(db=db, message=message, current_user=current_user)

    try:
        bot = Bot(token=created_message.bot_token)
    except TokenValidationError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid bot token provided")

    try:
        await bot.send_message(chat_id=created_message.chat_id, text=created_message.text)
    except TelegramBadRequest:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid chat id provided")
    finally:
        await bot.session.close()

    return created_message
