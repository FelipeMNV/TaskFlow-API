from http import HTTPStatus

from fast_zero.models import User
from fast_zero.security import get_password_hash


def test_token_wrong_email(client):
    response = client.post(
        '/auth/token',
        data={'username': 'nao_existo@example.com', 'password': 'password123'},
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Incorrect email or password'}


def test_token_wrong_password(client, user):
    response = client.post(
        '/auth/token',
        data={'username': user.email, 'password': 'wrong_password'},
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Incorrect email or password'}


def test_update_user_wrong_user(client, user, token, session):
    other_user = User(
        username='outro',
        email='outro@example.com',
        password=get_password_hash('password'),
    )
    session.add(other_user)
    session.commit()
    session.refresh(other_user)

    response = client.put(
        f'/users/{other_user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'novo_nome',
            'email': 'novo@example.com',
            'password': 'password',
        },
    )
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Not enough permissions'}


def test_get_token(client, user):
    response = client.post(
        '/auth/token',
        data={'username': user.email, 'password': user.clean_password},
    )
    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert token['token_type'] == 'Bearer'
    assert 'access_token' in token
