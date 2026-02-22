from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordRequestForm

from app.core.dependencies import get_db
from app.services.auth_service import AuthService
from app.domain.schemas.user import UserCreate, UserLogin, Token

router = APIRouter(prefix="/auth", tags=["Auth"])

auth_service = AuthService()

@router.post("/signup")
async def signup(data: UserCreate, db: AsyncSession = Depends(get_db)):
    try:
        user = await auth_service.signup(
            db,
            data.email,
            data.password,
        )
        return {"id":user.id, "email":user.email}

    except ValueError as e:
        return HTTPException(status_code=400, detail=str(e))

@router.post("/login", response_model=Token)
async def login(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db:AsyncSession = Depends(get_db),
):
    print("\n--- LOGIN ROUTE START ---")

    token = await auth_service.login(
            db,
            form_data.username,
            form_data.password,
        )
    print("TOKEN RETURNED FROM SERVICE:", token)

    return {
        "access_token": token,
        "token_type": "bearer",
    }
