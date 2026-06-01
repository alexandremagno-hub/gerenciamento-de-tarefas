from http import HTTPStatus

from freezegun import freeze_time


# TESTE DE LOGIN (TOKEN)
def test_get_token(client, user):
    # Faz login com usuário válido
    response = client.post(
        '/auth/token',
        data={'username': user.email, 'password': user.clean_password},
    )
    token = response.json()

    # Verifica sucesso
    assert response.status_code == HTTPStatus.OK
    # Verifica se retornou token
    assert 'access_token' in token
    # Verifica tipo do token
    assert 'token_type' in token


# SENHA ERRADA
def test_token_wrong_password(client, user):
    # Tenta login com senha errada
    response = client.post(
        '/auth/token',
        data={'username': user.email, 'password': 'wrong_password'},
    )
    # Deve falhar
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    # Mensagem genérica (boa prática de segurança)
    assert response.json() == {'detail': 'Incorrect email or password'}


# USUÁRIO INEXISTENTE
def test_token_inexistent_user(client):
    # Login com usuário que não existe
    response = client.post(
        '/auth/token',
        data={'username': 'no_user@no_domain.com', 'password': 'testtest'},
    )
    # Deve falhar
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    # Mesma mensagem (evita enumeração de usuários)
    assert response.json() == {'detail': 'Incorrect email or password'}


# REFRESH TOKEN
def test_refresh_token(client, token):
    # Solicita novo token com token válido
    response = client.post(
        '/auth/refresh_token',
        headers={'Authorization': f'Bearer {token}'},
    )

    data = response.json()

    # Verifica sucesso
    assert response.status_code == HTTPStatus.OK
    # Verifica retorno correto
    assert 'access_token' in data
    assert 'token_type' in data
    assert data['token_type'] == 'Bearer'


# TOKEN EXPIRADO
def test_token_expired_dont_refresh(client, user):
    # Congela o tempo na criação do token
    with freeze_time('2026-12-31 12:00:00'):
        response = client.post(
            '/auth/token',
            data={'username': user.email, 'password': user.clean_password},
        )
        assert response.status_code == HTTPStatus.OK
        # Guarda token criado nesse momento
        token = response.json()['access_token']

    # Avança o tempo além da expiração (31 minutos depois)
    with freeze_time('2026-12-31 12:31:00'):
        response = client.post(
            '/auth/refresh_token',
            headers={'Authorization': f'Bearer {token}'},
        )
        # Token expirado → não pode usar refresh
        assert response.status_code == HTTPStatus.UNAUTHORIZED
        # Mensagem padrão
        assert response.json() == {'detail': 'Could not validate credentials'}
