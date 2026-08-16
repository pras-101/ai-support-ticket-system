from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db_session
from app.models.user import User, UserRole
from app.schemas.auth import LoginRequest, RegisterRequest, TokenRead, UserRead
from app.services.auth import create_access_token, get_current_user, hash_password, verify_password

router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register_customer(
    registration: RegisterRequest, session: AsyncSession = Depends(get_db_session)
) -> User:
    existing_user = await session.scalar(select(User).where(User.username == registration.username))
    if existing_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username is already taken")

    # Public registration creates customers only. Agent/admin accounts are provisioned by an admin.
    user = User(
        username=registration.username,
        password_hash=hash_password(registration.password),
        role=UserRole.CUSTOMER,
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


@router.post("/login", response_model=TokenRead)
async def login(credentials: LoginRequest, session: AsyncSession = Depends(get_db_session)) -> TokenRead:
    user = await session.scalar(select(User).where(User.username == credentials.username))
    if user is None or not verify_password(credentials.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    return TokenRead(access_token=create_access_token(user))


@router.get("/me", response_model=UserRead)
async def read_current_user(current_user: User = Depends(get_current_user)) -> User:
    return current_user
