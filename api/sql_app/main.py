
from .models.user import user_model
from fastapi import FastAPI
from sql_app.api.api_v1.api import api_router
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from .database import engine
from sql_app.utils import project_root_dir

user_model.Base.metadata.create_all(bind=engine)

app = FastAPI(title='Project X')


app.mount(
    "/uploads", StaticFiles(directory=f"{project_root_dir}/sql_app/uploads"), name="static")

origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(api_router)
