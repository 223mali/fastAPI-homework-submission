from sqlalchemy.orm import Session
from fastapi import HTTPException
from ...models import Assignment
from sql_app.schemas import CreateAssignment


def create_assignment(db: Session, assignment: CreateAssignment) -> Assignment:
    if (not assignment.name):
        raise HTTPException(
            status_code=400, detail="Please provide an assignment name")

    if (not assignment.description):
        raise HTTPException(
            status_code=400, detail="Please provide an assignment description")

    db_assignment = Assignment(name=assignment.name,
                               description=assignment.description)

    db.add(db_assignment)
    db.commit()
    db.refresh(db_assignment)

    return db_assignment


def fetch_assignments(db: Session):
    return db.query(Assignment).all()
