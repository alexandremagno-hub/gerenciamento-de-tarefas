from contextlib import contextmanager
from datetime import datetime

import factory
import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy import event
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from testcontainers.postgres import PostgresContainer

from fastapi_zero.app import app
from fastapi_zero.database import get_session
from fastapi_zero.models import User, table_registry
from fastapi_zero.security import get_password_hash


# CLIENTE DE TESTE
@pytest.fixture
def client(session):
    # Override da dependência do banco
    def get_session_override():
        return session

    # Cria cliente HTTP de teste
    with TestClient(app) as client:
        # Substitui o get_session original pelo de teste
        app.dependency_overrides[get_session] = get_session_override
        yield client

    # Limpa override após o teste
    app.dependency_overrides.clear()


# ENGINE (BANCO TEMPORÁRIO)
@pytest.fixture(scope='session')
def engine():
    # Cria container PostgreSQL (isolado)
    with PostgresContainer('postgres:17', driver='psycopg') as postgres:
        # Cria engine async com URL do container
        _engine = create_async_engine(postgres.get_connection_url())
        yield _engine


# SESSÃO DE BANCO
@pytest_asyncio.fixture
async def session(engine):
    # Cria tabelas antes do teste
    async with engine.begin() as conn:
        await conn.run_sync(table_registry.metadata.create_all)

    # Abre sessão
    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session

    # Remove tabelas depois do teste
    async with engine.begin() as conn:
        await conn.run_sync(table_registry.metadata.drop_all)


# MOCK DE TEMPO
@contextmanager
def _mock_db_time(model, time=datetime(2024, 1, 1)):

    # Hook que altera created_at antes de inserir
    def fake_time_hook(mapper, connection, target):
        if hasattr(target, 'created_at'):
            target.created_at = time

    # Ativa hook
    event.listen(model, 'before_insert', fake_time_hook)

    yield time
    # Remove hook depois
    event.remove(model, 'before_insert', fake_time_hook)


@pytest.fixture
def mock_db_time():
    return _mock_db_time


# USUÁRIO DE TESTE
@pytest_asyncio.fixture
async def user(session):
    password = 'testtest'
    # Cria usuário fake
    user = UserFactory(password=get_password_hash(password))

    session.add(user)
    await session.commit()
    await session.refresh(user)

    # Guarda senha limpa para login
    user.clean_password = password

    return user


# Outro usuário (para testar autorização)
@pytest_asyncio.fixture
async def other_user(session):
    password = 'testtest'
    user = UserFactory(password=get_password_hash(password))

    session.add(user)
    await session.commit()
    await session.refresh(user)

    user.clean_password = password

    return user


# TOKEN JWT
@pytest.fixture
def token(client, user):
    response = client.post(
        '/auth/token',
        data={'username': user.email, 'password': user.clean_password},
    )
    return response.json()['access_token']


@pytest.fixture
def settings():
    return settings


# FACTORY DE USUÁRIO
class UserFactory(factory.Factory):
    class Meta:
        model = User
    # Username único
    username = factory.Sequence(lambda n: f'test{n}')
    # Email baseado no username
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@test.com')
    # Senha fake (depois será hash)
    password = factory.LazyAttribute(lambda obj: f'{obj.username}@example.com')
