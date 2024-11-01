from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy import select

from src.database import async_session_factory
from src.users.dependencies import check_auth_header
from src.users.models import User
from src.users.schemas import UserGetScheme, UserCreateScheme

router = APIRouter(
    prefix="/users",
    tags=["Users"],
    dependencies=[Depends(check_auth_header)],
    responses={404: {"description": "Not found"}},
)


@router.post("/")
async def create_user(new_user_data: UserCreateScheme, referrer_id: Optional[int] = None):
    async with async_session_factory() as session:
        existing_user = await session.execute(
            select(User).where(User.id == new_user_data.id)
        )
        existing_user = existing_user.scalar()
        if existing_user:
            return {
                "status": "error",
                "message": "User already exists"
            }

        new_user = User(id=new_user_data.id)

        if referrer_id:
            referrer = await session.execute(
                select(User).where(User.id == referrer_id)
            )
            referrer = referrer.scalar()
            if referrer:
                new_user.referrer = referrer

        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)

        return {
            "status": "success",
            "message": "User successfully created",
            "data": {"user": UserGetScheme.model_validate(new_user).model_dump()}
        }


@router.get("/{user_id}")
async def get_user(user_id: int):
    async with async_session_factory() as session:
        user = await session.execute(
            select(User).where(User.id == user_id)
        )
        user = user.scalar()
        if not user:
            return {
                "status": "error",
                "message": "User not found"
            }

        return {
            "status": "success",
            "data": {"user": UserGetScheme.model_validate(user).model_dump()}
        }


@router.get("/test-auth")
async def test_auth():
    return {"message": "You are authenticated"}
