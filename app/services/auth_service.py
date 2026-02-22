from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.domain.models.user import User
from app.core.security import hash_password, verify_password, create_access_token

class AuthService:
    async def signup(self, db: AsyncSession, email: str, password: str):

        print("\n--- SIGNUP DEBUG ---")
        print("PASSWORD VALUE:", password)
        print("TYPE:", type(password))

        result = await db.execute(select(User).where(User.email == email))
        existing = result.scalar_one_or_none()

        if existing:
            raise ValueError("User already exists")

        # IMPORTANT: force string
        clean_password = str(password)

        hashed_password = hash_password(clean_password)

        user = User(
            email=email,
            hashed_password=hashed_password,
        )

        db.add(user)
        await db.commit()
        await db.refresh(user)

        return user

    async def login(self, db:AsyncSession, email:str, password:str):
        print("\n--- LOGIN DEBUG ---")
        print("INPUT EMAIL:", email)
        print("INPUT PASSWORD:", password)
        result = await db.execute(select(User).where(User.email == email))
        user = result.scalar_one_or_none()
        print("USER OBJECT:", user)

        if user is None:
            raise ValueError("Invalid Credentials")

        is_valid = verify_password(password, user.hashed_password)
        print("VERIFY RESULT:", is_valid)

        if not is_valid:
            raise ValueError("Invalid Credentials")

        token = create_access_token({"sub": str(user.id)})
        print("TOKEN CREATED SUCCESSFULLY")

        return token
