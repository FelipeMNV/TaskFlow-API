from sqlalchemy import select

from fast_zero.database import get_session
from fast_zero.models import User


def test_create_user(session, mock_db_time):

    with mock_db_time(model=User) as time:
        new_user = User(
            username='teste',
            email='teste@test',
            password='secret',
        )
        session.add(new_user)
        session.commit()

    user = session.scalar(select(User).where(User.username == 'teste'))

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


def test_get_session():
    for session in get_session():
        assert session is not None
