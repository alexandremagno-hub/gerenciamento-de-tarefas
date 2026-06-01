from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_zero.database import get_session
from fastapi_zero.models import User
from fastapi_zero.schemas import (
    FilterPage,
    Message,
    UserList,
    UserPublic,
    UserSchema,
)

# Segurança (usuário atual + hash de senha)
from fastapi_zero.security import (
    get_current_user,
    get_password_hash,
)

# Agrupa rotas com prefixo /users
router = APIRouter(prefix='/users', tags=['users'])

# Usuário autenticado
CurrentUser = Annotated[User, Depends(get_current_user)]
# Sessão do banco
SessionDep = Annotated[AsyncSession, Depends(get_session)]


# Cria usuários
@router.post(
    '/',
    status_code=HTTPStatus.CREATED,
    response_model=UserPublic,
)
async def create_user(
    user: UserSchema,  # Dados recebidos
    session: SessionDep,
):
    # Verifica se já existe usuáro com o mesmo username ou email
    db_user = await session.scalar(
        select(User).where((User.username == user.username) | (User.email == user.email))
    )

    if db_user:
        # Username já existe
        if db_user.username == user.username:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='Username already exists',
            )
        # Email já existe
        elif db_user.email == user.email:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='Email already exists',
            )

    # Cria novo usuário com senha criptografada
    db_user = User(
        username=user.username,
        email=user.email,
        password=get_password_hash(user.password),
    )
    session.add(db_user)  # salva no banco
    await session.commit()  # adciona no banco
    await session.refresh(db_user)  # atualiza no banco

    return db_user


# Lista usuários
@router.get(
    '/',
    response_model=UserList,
)
async def read_users(
    session: SessionDep,
    # Query params (?offset=0&limit=10)
    filter_users: Annotated[
        FilterPage,
        Query(),
    ],
):
    # Busca usuários com paginação
    query = await session.scalars(
        select(User).offset(filter_users.offset).limit(filter_users.limit)
    )
    users = query.all()

    return {'users': users}


# Atualiza usuários
@router.put(
    '/{user_id}',
    response_model=UserPublic,
)
async def update_user(
    user_id: int,
    user: UserSchema,
    session: SessionDep,
    current_user: CurrentUser,
):
    # Impede editar outro usuário
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='Not enough permissions',
        )

    try:
        # Atualiza dados
        current_user.username = user.username
        current_user.password = get_password_hash(user.password)
        current_user.email = user.email
        await session.commit()
        await session.refresh(current_user)

        return current_user

    # Caso username/email já exista
    except IntegrityError:
        raise HTTPException(
            detail='Username or Email already exists',
            status_code=HTTPStatus.CONFLICT,
        )


# Deleta usuários
@router.delete(
    '/{user_id}',
    status_code=HTTPStatus.OK,
    response_model=Message,
)
async def delete_user(
    user_id: int,
    session: SessionDep,
    current_user: CurrentUser,
):
    # Impede deletar outro usuário
    if current_user.id != user_id:
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail='Not enough permissions')

    # Remove do banco
    await session.delete(current_user)
    await session.commit()

    return {'message': 'User deleted'}
