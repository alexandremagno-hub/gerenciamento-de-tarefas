from datetime import datetime, timedelta
from http import HTTPStatus
from zoneinfo import ZoneInfo

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import DecodeError, ExpiredSignatureError, decode, encode
from pwdlib import PasswordHash
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_zero.database import get_session
from fastapi_zero.models import User
from fastapi_zero.settings import Settings

settings = Settings()

# Contexto de hash (configuração segura padrão)
pwd_context = PasswordHash.recommended()

# Define como o token será obtido (header Authorization: Bearer <token>)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/token')


# HASH DE SENHA
def get_password_hash(password: str):
    # Gera hash da senha
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    # Compara senhas digitadas com hash
    return pwd_context.verify(plain_password, hashed_password)


# USUÁRIO ATUAL (AUTENTICAÇÃO)
async def get_current_user(
    session: AsyncSession = Depends(get_session),  # sessão do banco
    token: str = Depends(oauth2_scheme),  # token vindo do header
):
    # exceção padrão de erro de autenticação
    credentials_exception = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )

    try:
        # Decodifica o token JWt
        payload = decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )
        # Pega o "sub" (subject = identificador do usuário)
        subject_email = payload.get('sub')

        # Se não tiver email no token → inválido
        if not subject_email:
            raise credentials_exception

    # Token inválido (formato errado)
    except DecodeError:
        raise credentials_exception

    # Token expirado
    except ExpiredSignatureError:
        raise credentials_exception

    # Busca usuário no banco pelo email
    user = await session.scalar(select(User).where(User.email == subject_email))

    # Se não encontrar usuário → inválido
    if not user:
        raise credentials_exception

    # Retorna o usuário autenticado
    return user


# CRIAÇÃO DO TOKEN JWT
def create_access_token(data: dict):
    # Copia os dados (ex: {"sub": email})
    to_encode = data.copy()
    # Define tempo de expiração
    expire = datetime.now(tz=ZoneInfo('UTC')) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    # Adiciona expiração ao payload
    to_encode.update({'exp': expire})
    # Cria o token JWT
    encoded_jwt = encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )
    return encoded_jwt
