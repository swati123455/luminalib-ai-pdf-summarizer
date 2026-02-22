from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from app.core.config import get_settings
from app.infrastructure.db.session import engine
from app.infrastructure.db.base_class import Base
from app.infrastructure.db import base

from app.api.v1.health import router as health_router
import app.infrastructure.db
from app.api.v1.auth import router as auth_router
from app.api.v1.books import router as book_router

from app.core.auth_dependencies import get_current_user
from app.domain.models.user import User
from fastapi import Depends



settings = get_settings()
app = FastAPI(title=settings.app_name)

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get("/")
async def root():
    return {"message" : "LuminaLib API running"}

@app.get("/protected")
async def protected_route(current_user: User = Depends(get_current_user)):
    return {"message" : f"Hello {current_user.email}"}

app.include_router(health_router)
app.include_router(auth_router)
app.include_router(book_router)