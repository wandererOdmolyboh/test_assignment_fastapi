from pydantic import BaseModel


class MessageCreate(BaseModel):
    text: str
    chat_id: str
    bot_token: str
    user_id: int


class Message(BaseModel):
    id: int
    text: str
    chat_id: str
    bot_token: str
