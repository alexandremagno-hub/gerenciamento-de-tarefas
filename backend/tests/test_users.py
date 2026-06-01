from http import HTTPStatus

from fastapi_zero.schemas import UserPublic


# CRIAÇÃO DE USUÁRIO
def test_create_user(client):  # client simula um navegador/API client
    response = client.post(
        '/users/',
        json={
            'username': 'alice',
            'email': 'alice@example.com',
            'password': 'secret',
        },
    )
    # Verifica criação
    assert response.status_code == HTTPStatus.CREATED
    # Verifica retorno (sem senha)
    assert response.json() == {
        'username': 'alice',
        'email': 'alice@example.com',
        'id': 1,
    }


# LISTAGEM SEM USUÁRIOS
def test_read_users(client):
    response = client.get('/users')
    assert response.status_code == HTTPStatus.OK
    # Deve retornar lista vazia
    assert response.json() == {'users': []}


# LISTAGEM COM USUÁRIOS
def test_read_users_with_users(client, user):
    # Converte o model para o formato da API
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/')
    # Verifica se o usuário aparece na lista
    assert response.json() == {'users': [user_schema]}


# ATUALIZAÇÃO DE USUÁRIO
def test_update_user(client, user, token):
    response = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},  # Envia token JWT
        json={
            'username': 'bob',
            'email': 'bob@example.com',
            'password': 'mynewpassword',
        },
    )
    assert response.status_code == HTTPStatus.OK
    # Verifica dados atualizados
    assert response.json() == {
        'username': 'bob',
        'email': 'bob@example.com',
        'id': 1,
    }


# ERRO DE INTEGRIDADE (duplicado)
def test_update_integrity_error(client, user, token):
    # Cria outro usuário
    client.post(
        '/users/',
        json={
            'username': 'fausto',
            'email': 'fausto@example.com',
            'password': 'secret',
        },
    )

    # Tenta atualizar com username duplicado
    response_update = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'fausto',
            'email': 'bob@example.com',
            'password': 'mynewpassword',
        },
    )
    # Deve dar conflito
    assert response_update.status_code == HTTPStatus.CONFLICT
    assert response_update.json() == {'detail': 'Username or Email already exists'}


# DELETE SUCESSO
def test_delete_user(client, user, token):
    response = client.delete(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}


# ATUALIZAÇÃO SEM PERMISSÃO
def test_update_user_with_wrong_user(client, other_user, token):
    # Tenta atualizar outro usuário
    response = client.put(
        f'/users/{other_user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'bob',
            'email': 'bob@example.com',
            'password': 'mynewpassword',
        },
    )
    # Deve bloquear
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Not enough permissions'}


# DELETE SEM PERMISSÃO
def test_delete_user_wrong_user(client, other_user, token):
    response = client.delete(
        f'/users/{other_user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )
    # Deve bloquear
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Not enough permissions'}
