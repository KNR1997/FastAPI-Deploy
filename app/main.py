from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database import init_db, close_db
from app.models import User, Todo


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()   # connect + auto-create tables
    yield
    await close_db()  # disconnect


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def read_root():
    return {"message": "Hello, Tortoise ORM with generate_schemas!"}


@app.post("/users/")
async def create_user(name: str, email: str):
    user = await User.create(name=name, email=email)
    return {"id": user.id, "name": user.name, "email": user.email}
