import os

from typing import Dict
from jose import jwt, JWTError
from datetime import datetime, timedelta
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv

from api.schema import TokenData, db

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM_HASH = os.getenv("ALGORITHM_HASH")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def create_access_token(payload: dict):
    to_encode = payload.copy()
    expiration_time = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expiration_time})
    jwt_token = jwt.encode(to_encode, key=SECRET_KEY, algorithm=ALGORITHM_HASH)
    return jwt_token


def verify_access_token(token: str, credential_exception: Dict):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM_HASH])

        id: str = payload.get("id")

        if not id:
            raise credential_exception

        token_data = TokenData(id=id)
        return token_data
    except JWTError:
        raise credential_exception


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not verify token, token expired",
        headers={
            "WWW-AUTHENTICATE": "Bearer",
        },
    )

    current_user_id = verify_access_token(
        token=token, credential_exception=credential_exception
    ).id

    current_user = await db["users"].find_one({"_id": current_user_id})

    return current_user
