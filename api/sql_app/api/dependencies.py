
from typing import List
from sql_app.api.constants import ALGORITHM

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from sql_app.controllers.user import authentication

from sql_app.database import SessionLocal, engine
from .constants import SECRET_KEY, ALGORITHM


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/token")


async def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY,
                             algorithms=[ALGORITHM])
        print(payload)
        username: str = payload.get("email")
        if username is None:

            raise credentials_exception
        token_data = username

    except JWTError:
        raise credentials_exception
    user = authentication.get_user(db, email=token_data)
    if user is None:
        raise credentials_exception
    return user


async def get_current_user_teacher(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Only Teachers can perform this action",
        headers={"WWW-Authenticate": "Bearer"},
    )
    user = await get_current_user(db, token)
    print(user.role)
    if user.role.lower() == 'teacher':
        return user
    else:
        raise credentials_exception
