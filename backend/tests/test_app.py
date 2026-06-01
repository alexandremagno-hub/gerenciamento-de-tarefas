from http import HTTPStatus


# TESTE DA ROTA RAIZ
def test_root_deve_retornar_ola_mundo(client):
    # Faz requisição GET na raiz
    response = client.get('/')

    # Verifica o corpo da resposta
    assert response.json() == {'message': 'Olá Mundo!'}
    # Verifica status HTTP 200
    assert response.status_code == HTTPStatus.OK


# TESTE DE CRIAÇÃO DE USUÁRIO
def test_create_user(client):
    # Envia POST para criar usuário
    response = client.post(
        '/users/',
        json={
            'username': 'alice',
            'email': 'alice@example.com',
            'password': 'secret',
        },
    )
    # Verifica status 201 (criado)
    assert response.status_code == HTTPStatus.CREATED
    # Verifica resposta (sem senha)
    assert response.json() == {
        'id': 1,
        'username': 'alice',
        'email': 'alice@example.com',
    }


# TESTE DE LISTAGEM DE USUÁRIOS
def test_read_users(client, user, token):
    # Faz GET com autenticação
    response = client.get(
        '/users/',
        headers={'Authorization': f'Bearer {token}'},
    )
    # Verifica sucesso
    assert response.status_code == HTTPStatus.OK
    # Verifica se retorna o usuário criado
    assert response.json() == {
        'users': [
            {
                'id': user.id,
                'username': user.username,
                'email': user.email,
            },
        ],
    }


# TESTE DE ATUALIZAÇÃO
def test_update_user(client, user, token):
    # Atualiza dados do usuário
    response = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'bob',
            'email': 'bob@example.com',
            'password': 'secret',
        },
    )
    # Verifica sucesso
    assert response.status_code == HTTPStatus.OK
    # Verifica dados atualizados
    assert response.json() == {
        'id': user.id,
        'username': 'bob',
        'email': 'bob@example.com',
    }


# TESTE DE DELEÇÃO
def test_delete_user(client, user, token):
    # Deleta usuário
    response = client.delete(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    # Verifica sucesso
    assert response.status_code == HTTPStatus.OK
    # Verifica mensagem
    assert response.json() == {'message': 'User deleted'}


# TESTE DE ERRO DE INTEGRIDADE
def test_update_integrity_error(client, user, token):
    # Cria outro usuário com username/email específico
    client.post(
        '/users/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'fausto',
            'email': 'fausto@example.com',
            'password': 'secret',
        },
    )

    # Tenta atualizar com username duplicado
    response = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'fausto',
            'email': 'bob@example.com',
            'password': 'mynewpassword',
        },
    )
    # Verifica erro 409 (conflito)
    assert response.status_code == HTTPStatus.CONFLICT
    # Verifica mensagem de erro
    assert response.json() == {'detail': 'Username or Email already exists'}


# TESTE DE LOGIN (TOKEN)
def test_get_token(client, user):
    response = client.post(
        '/auth/token',
        data={'username': user.email, 'password': user.clean_password},
    )
    token = response.json()

    # Verifica sucesso
    assert response.status_code == HTTPStatus.OK
    # Verifica tipo do token
    assert token['token_type'] == 'Bearer'
    # Verifica existência do access_token
    assert 'access_token' in token
