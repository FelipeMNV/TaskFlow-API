from http import HTTPStatus


def test_read_root_deve_retornar_OK_e_ola_mundo(client):

    response = client.get('/')  # Action

    assert response.status_code == HTTPStatus.OK  # Assert
    assert response.json() == {'message': 'Olá Mundo!'}  # Assert
