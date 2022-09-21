from sql_app.api.dependencies import get_current_user_teacher
from sql_app.api.constants import ACCESS_TOKEN_EXPIRE_MINUTES
from sql_app.api.dependencies import get_current_user, get_db
from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from datetime import timedelta

from sql_app import models, schemas
from sql_app.controllers.user import authentication


router = APIRouter()


@router.post("/token", response_model=schemas.Token)
async def login_for_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = authentication.authenticate_user(
        db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(days=ACCESS_TOKEN_EXPIRE_MINUTES)
    dataDict = {"first_name": user.first_name,
                "last_name": user.last_name, "email": user.email, 'id': user.id}
    access_token = authentication.create_access_token(
        data=dataDict, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/me/")
async def read_users_me(current_user: models.User = Depends(get_current_user_teacher)):
    return current_user


@router.post("/user")
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return authentication.create_user(db=db, user=user)


@router.get("/users")
def get_users(db: Session = Depends(get_db)):
    return authentication.get_users(db=db)
