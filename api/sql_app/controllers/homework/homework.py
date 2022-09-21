from ast import And
from datetime import datetime
from os import getcwd
from sqlalchemy.orm import Session
from sqlalchemy import update
from os.path import exists
from sql_app.utils import convert_date
from sql_app.models.assignment.assignment_model import Assignment
from sql_app.schemas.user.user_schemas import User
from sql_app.models.homework.homework_model import grade_enum
from fastapi import HTTPException, status
from ...models import Homework
from sql_app.schemas import SubmitHomeWork


def create_homework(db: Session, payload: SubmitHomeWork, current_user: User) -> Homework:
    if not exists(f'{getcwd()}/sql_app/uploads/{payload.filename}'):
        raise HTTPException(status_code=400,
                            detail="UPload your homework attachement")
    db_assignment = db.query(Assignment).filter(
        Assignment.id == payload.assignment_id).first()
    print(db_assignment.name)
    if (not db_assignment):
        raise HTTPException(
            status_code=400, detail="The assignment that you are trying to submit does not exist")

    db_homework = Homework(student_name=f"{current_user.first_name} {current_user.last_name}", homework_name=db_assignment.name,
                           file_path=payload.file_path, finale_grade=grade_enum.Ungraded, assignment_id=payload.assignment_id, user_id=current_user.id)

    db.add(db_homework)
    db.commit()
    db.refresh(db_homework)

    return db_homework


def fetch_homeworks(db: Session, name: str, from_date: str, to_date: str, student: str):
    db_response = db.query(Homework)
    if name:
        db_response = db_response.filter(Homework.homework_name.contains(name))
    if (from_date):
        print('check')
        db_response = db_response.filter(
            Homework.submission_date >= (convert_date(from_date)))
    if (to_date):
        db_response = db_response.filter(
            Homework.submission_date <= (convert_date(to_date, '%d-%m-%Y')))
    if student:
        db_response = db_response.filter(
            Homework.student_name.contains(student))
    return db_response.all()


def grade_homeworks(db: Session, homework_id: int, grade: str, notes):
    if (grade_enum(grade)):
        print(grade)

        stmt = update(Homework).where(Homework.id == homework_id).values(finale_grade=grade, teacher_notes=notes).\
            execution_options(synchronize_session="fetch")
        db.execute(stmt)
        db.commit()
        return db.query(Homework).filter(Homework.id == homework_id).first()


def fetch_student_homework(db, student_id, grade_filter=None, name_filter=None):
    if (grade_filter):
        return db.query(Homework).filter(Homework.user_id == student_id).filter(Homework.finale_grade == grade_filter).all()
    if (name_filter):
        return db.query(Homework).filter(Homework.user_id == student_id).filter(Homework.homework_name.contains(name_filter)).all()
    return db.query(Homework).filter(Homework.user_id == student_id).all()
