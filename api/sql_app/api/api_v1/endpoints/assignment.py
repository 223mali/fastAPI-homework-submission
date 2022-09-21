from sql_app.api.dependencies import get_db, get_current_user_teacher
from fastapi import Depends,  APIRouter
from sqlalchemy.orm import Session
from sql_app import models, schemas
from sql_app.controllers.assignment import assignment


router = APIRouter()


@router.post("/assignment", response_model=schemas.ReturnedAssignment)
async def create_assignment(payload: schemas.CreateAssignment, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user_teacher)):
    payload = assignment.create_assignment(db, payload)
    return payload


@router.get("/", response_model=list[schemas.ReturnedAssignment])
async def fetch_assignments(db: Session = Depends(get_db)):
    payload = assignment.fetch_assignments(db)
    return payload
