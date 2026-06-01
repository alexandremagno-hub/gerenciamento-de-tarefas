from http import HTTPStatus

from jwt import decode

from fastapi_zero.security import create_access_token, settings


# TESTE DE CRIAÇÃO DO JWT
def test_jwt():

    # Dados que vão dentro do token
    data = {'test': 'test'}
    # Cria token JWT
    token = create_access_token(data)
    # Decodifica token usando a mesma chave e algoritmo
    decoded = decode(
        token,
        settings.SECRET_KEY,
        algorithms=[settings.ALGORITHM]
    )
    # Verifica se os dados foram preservados
    assert decoded['test'] == data['test']
    # Verifica se existe campo de expiração
    assert 'exp' in decoded


# TESTE DE TOKEN INVÁLIDO
def test_jwt_invalid_token(client):
    # Faz requisição com token inválido
    response = client.delete('/users/1', headers={'Authorization': 'Bearer token-invalido'})

    # Deve retornar erro de autenticação
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    # Mensagem padrão de segurança
    assert response.json() == {
        'detail': 'Could not validate credentials'
    }
