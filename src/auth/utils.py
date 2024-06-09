
import jwt
from jwt import PyJWTError
from typing import Any, Dict


def get_token_data(token: str, secret_key: str, algorithm: str) -> Dict[str, Any]:
    try:
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
    except PyJWTError:
        raise ValueError("Could not decode token. Invalid token or secret key.")
    return payload
