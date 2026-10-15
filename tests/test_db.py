import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import (
    AsyncSession,
)

from fast_zero.database import get_session
from fast_zero.models import User


@pytest.mark.asyncio
async def test_create_user(session: 'AsyncSession', mock_db_time):

    with mock_db_time(model=User) as time:
        new_user = User(
            username='teste',
            email='teste@test',
            password='secret',
        )
        session.add(new_user)
        await session.commit()

    user = await session.scalar(select(User).where(User.username == 'teste'))

    user_dict = {
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'password': user.password,
        'created_at': user.created_at,
        'updated_at': user.updated_at,
    }

    assert user_dict == {
        'id': 1,
        'username': 'teste',
        'email': 'teste@test',
        'password': 'secret',
        'created_at': time,
        'updated_at': time,
    }


@pytest.mark.asyncio
async def test_get_session():
    async for session in get_session():
        assert isinstance(session, AsyncSession)
