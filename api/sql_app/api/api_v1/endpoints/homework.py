from datetime import date, datetime
from os import getcwd
from typing import Optional
from sql_app.api.dependencies import get_current_user_teacher
from sql_app.schemas.user.user_schemas import User
from sql_app.api.dependencies import get_db, get_current_user
from fastapi import Depends,  APIRouter, UploadFile
from sqlalchemy.orm import Session
from sql_app import models, schemas
from sql_app.controllers.assignment import assignment
from sql_app.controllers.homework import homework
from sql_app.utils import project_root_dir
import uuid
router = APIRouter()

# Using a rsponse model here kept giving me a pydantic error. the error message was kryptic so removing the reponse model allowed me to return value


@router.post("/homework")
async def create_homework(payload: schemas.SubmitHomeWork, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    payload = homework.create_homework(db, payload, current_user)
    print(payload.id)
    return payload


@router.get("/all")
async def fetch_homeWorks(name: str = None, from_date: str = None, to_date: str = None, student: str = None, db: Session = Depends(get_db)):
    return homework.fetch_homeworks(db, name, from_date, to_date, student)


@router.get("/user/all")
async def fetch_student_homeworks(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return homework.fetch_student_homework(db, student_id=current_user.id)


@router.get("/user/all/filter/grade/{grade}")
async def fetch_student_homeworks(grade, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return homework.fetch_student_homework(db, student_id=current_user.id, grade_filter=grade)


@router.get("/user/all/filter/name/{name}")
async def fetch_student_homeworks(name, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return homework.fetch_student_homework(db, student_id=current_user.id, name_filter=name)


@router.post("/homework/grade")
async def grade_homeworks(payload: schemas.GradeHomework, db: Session = Depends(get_db), current_user: User = Depends(get_current_user_teacher)):
    return homework.grade_homeworks(db, homework_id=payload.homework_id, grade=payload.finale_grade, notes=payload.teacher_notes)


@router.post("/upload", response_model=schemas.UploadRes)
async def upload_file(file: UploadFile, current_user: User = Depends(get_current_user)):
    db_file_name = f'{current_user.id}-{current_user.first_name}-{uuid.uuid1()}-{file.filename}'
    try:
        contents = file.file.read()
        with open(f'{project_root_dir}/sql_app/uploads/{db_file_name}', 'xb') as f:
            f.write(contents)
    except Exception as e:
        print(e)
        return {"message": "something went wrong uploading the file"}
    finally:
        file.file.close()

    return {"file_path": f"http://localhost:8080/uploads/{db_file_name}",
            "message": "File uploaded successfuly",
            "filename": f"{db_file_name}"
            }
