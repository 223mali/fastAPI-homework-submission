from sqlalchemy.orm import Session
from ...models.user import user_model
from fastapi import HTTPException
from ...schemas import UserCreate
from ...models import User
from jose import jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional
from fastapi.security import OAuth2PasswordBearer
from sql_app.api.constants import SECRET_KEY, ALGORITHM

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def create_user(db: Session, user: UserCreate):
    userExist = get_user(db, user.email)
    if (userExist):
        raise HTTPException(
            status_code=409, detail="User email already exists")
    db_user = User(
        first_name=user.first_name, last_name=user.last_name,
        hashed_password=get_password_hash(user.password), email=user.email,
        role=user.role
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=1)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_user(db, email: str):
    return db.query(user_model.User).filter(user_model.User.email == email).first()


def get_user_by_id(db, uid: int):
    return db.query(user_model.User).filter(user_model.User.id == uid).first()


def get_users(db):
    return db.query(user_model.User).all()
