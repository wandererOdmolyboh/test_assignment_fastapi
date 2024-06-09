from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.message.models import DBMessage
from src.message.schemas import MessageCreate
from src.user.models import UserDB
from src.user.schemas import User


async def get_all_messages(db: AsyncSession):
    query = select(DBMessage)
    message_list = await db.execute(query)
    return [message[0] for message in message_list.fetchall()]


async def get_manager_all_messages(db: AsyncSession, manager_id: int):
    user_query = select(UserDB).where(UserDB.created_by == manager_id)
    user_list = await db.execute(user_query)
    user_ids = [user[0].id for user in user_list.fetchall()]
    user_ids.append(manager_id)

    message_query = select(DBMessage).where(DBMessage.user_id.in_(user_ids))
    message_list = await db.execute(message_query)
    return [message[0] for message in message_list.fetchall()]


async def get_user_all_messages(db: AsyncSession, user_id: int):
    query = select(DBMessage).where(DBMessage.user_id == user_id)
    message_list = await db.execute(query)
    return [message[0] for message in message_list.fetchall()]


async def create_message(db: AsyncSession, message: MessageCreate, current_user: User):
    query = (insert(DBMessage).values(text=message.text, chat_id=message.chat_id, bot_token=message.bot_token, user_id=current_user.id).returning(
        DBMessage.id))

    message_id = await db.execute(query)
    await db.commit()

    query = select(DBMessage).where(DBMessage.id == message_id.scalar_one())
    result = await db.execute(query)
    created_message = result.scalar_one()

    return created_message
