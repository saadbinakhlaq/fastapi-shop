from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.user import get_user, get_user_by_email, create_user, InUser

async def test_user(db_session: AsyncSession):
  in_user = InUser(
    username="testuser",
    email="testuser@gmail.com",
    first_name="test",
    last_name="user",
    hashed_password="123456",
    is_superuser=False,
    slug="testuser",
  )
  new_user = await create_user(db_session, in_user)
  user = await get_user(db_session, new_user.id)
  assert user.id == new_user.id
