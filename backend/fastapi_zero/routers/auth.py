from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_zero.database import get_session
from fastapi_zero.models import User
from fastapi_zero.schemas import Token
from fastapi_zero.security import (
    create_access_token,
    get_current_user,
    verify_password,
)

# Cria um roteador com prefixo "/auth"
# Todas as rotas aqui começam com /auth
router = APIRouter(prefix='/auth', tags=['auth'])

# Define um tipo reutilizável para sessão do banco
SessionDep = Annotated[AsyncSession, Depends(get_session)]

# Define um tipo para pegar dados do formulário OAuth2 (username/password)
OAuth2Form = Annotated[OAuth2PasswordRequestForm, Depends()]

# Define um tipo para pegar o usuário autenticado
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post(
    '/token',
    response_model=Token,
)
async def login_for_access_token(
    form_data: OAuth2Form,  # dados do formulário (username e password)
    session: SessionDep,  # sessão do banco
):
    # Busca o usuário no banco pelo email (username no OAuth2)
    user = await session.scalar(
        select(User).where(User.email == form_data.username)
    )

    # Se não encontrar o usuário
    if not user:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Incorrect email or password',
        )

    # Verifica se a senha está correta
    if not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Incorrect email or password',
        )

    # Cria um Token JWT com o e-mail do úsuario
    access_token = create_access_token(
        data={'sub': user.email}  # "sub" = subject (identificador do usuário)
    )

    # Retorna o token no padrão esperado
    return {'access_token': access_token, 'token_type': 'Bearer'}


# Rota para renovar o Token
@router.post(
    '/refresh_token',
    response_model=Token,
)
async def refresh_access_token(
    # Pega o usuário autenticado automaticamente pelo token
    user: Annotated[User, Depends(get_current_user)],
):
    # Gera um novo token com base no usuário atual
    new_access_token = create_access_token(data={'sub': user.email})

    # Retorna o novo token
    return {
        'access_token': new_access_token,
        'token_type': 'Bearer'
    }
