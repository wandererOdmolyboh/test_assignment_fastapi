from datetime import datetime, timedelta
from typing import Optional

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.config import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, JWT_SECRET
from src.dependencies import get_async_session
from src.user import crud as user_crud

oauth2_schema = OAuth2PasswordBearer(tokenUrl="/task_2/login")


def create_access_token(
        payload: dict,
        expires_delta: Optional[timedelta] = None
):
    to_encode = payload.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(payload=to_encode, key=JWT_SECRET, algorithm=ALGORITHM)

    return encoded_jwt


async def validate_token_from_headers(token: str = Depends(oauth2_schema)):
    return await validate_token(token)


async def validate_token(token):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
        user_id = int(payload.get("user_id"))
        return user_id
    except jwt.PyJWTError:
        return None


async def get_current_user(
        token: str = Depends(oauth2_schema),
        db: AsyncSession = Depends(get_async_session)
):
    user_id = await validate_token(token)
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    else:
        user = await user_crud.get_user_by_id(db, id=user_id)
        if user is None:
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )
        return user
