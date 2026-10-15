from http import HTTPStatus

import pytest

from fast_zero.models import User
from fast_zero.schemas import UserPublic
from fast_zero.security import get_password_hash


def test_read_root_deve_retornar_OK_e_ola_mundo(client):

    response = client.get('/')  # Action

    assert response.status_code == HTTPStatus.OK  # Assert
    assert response.json() == {'message': 'Olá Mundo!'}  # Assert


def test_create_user(client):

    response = client.post(
        '/users/',
        json={
            'username': 'alice',
            'email': 'alice@example.com',
            'password': 'secret',
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'email': 'alice@example.com',
        'username': 'alice',
    }


def test_create_user_already_exists_username(client, user):
    response = client.post(
        '/users/',
        json={
            'username': user.username,
            'email': 'outro_email@example.com',
            'password': 'secretpassword',
        },
    )
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Username already exists'}


def test_create_user_already_exists_email(client, user):
    response = client.post(
        '/users/',
        json={
            'username': 'outro_username',
            'email': user.email,
            'password': 'secretpassword',
        },
    )
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Email already exists'}


def test_read_users(client, user, token):

    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get(
        '/users/', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_schema]}


def test_update_user(client, user, token):
    response = client.put(
        '/users/1',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'bob',
            'email': 'bob@example.com',
            'password': 'mynewpassword',
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'bob',
        'email': 'bob@example.com',
        'id': 1,
    }


@pytest.mark.asyncio
async def test_get_user(client, user):
    response = client.get('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': user.username,
        'email': user.email,
        'id': user.id,
    }


def test_get_user_not_found(client, token):
    response = client.get(
        '/users/999', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


@pytest.mark.asyncio
async def test_delete_user(client, user, token):
    response = client.delete(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}


@pytest.mark.asyncio
async def test_delete_user_wrong_user(client, user, token, session):
    other_user = User(
        username='outrodel',
        email='outrodel@example.com',
        password='password',
    )
    session.add(other_user)
    await session.commit()
    await session.refresh(other_user)

    response = client.delete(
        f'/users/{other_user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Not enough permission'}


@pytest.mark.asyncio
async def test_update_integrity_error(client, user, token, session):
    other_user = User(
        username='outro',
        email='outro@example.com',
        password=get_password_hash('password'),
    )
    session.add(other_user)
    await session.commit()

    response = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'fausto',
            'email': 'outro@example.com',
            'password': 'mynewpassword',
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Username or Email already exists'}
