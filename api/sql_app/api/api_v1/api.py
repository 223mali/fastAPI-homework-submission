from fastapi import APIRouter

from sql_app.api.api_v1.endpoints import user, assignment, homework

api_router = APIRouter()
api_router.include_router(user.router, prefix="/users", tags=["users"])
api_router.include_router(
    assignment.router, prefix="/assignments", tags=["assignments"])
api_router.include_router(
    homework.router, prefix="/homeworks", tags=["homeworks"])
