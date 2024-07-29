from app.models import User as UserDBModel
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel


async def get_user(db_session: AsyncSession, user_id: int):
    user = (await db_session.scalars(select(UserDBModel).where(UserDBModel.id == user_id))).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


async def get_user_by_email(db_session: AsyncSession, email: str):
    return (await db_session.scalars(select(UserDBModel).where(UserDBModel.email == email))).first()


class InUser(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    hashed_password: str
    is_superuser: bool
    slug: str = ""


async def create_user(db_session: AsyncSession, user: InUser):
    db_user = UserDBModel(**user.model_dump())
    db_session.add(db_user)
    await db_session.commit()
    await db_session.refresh(db_user)
    return db_user
