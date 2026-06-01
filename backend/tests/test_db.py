from dataclasses import asdict

import pytest
from sqlalchemy import select

from fastapi_zero.models import Todo, User


# TESTE DE CRIAÇÃO DE USER
@pytest.mark.asyncio
async def test_create_user(session, mock_db_time):
    # Congela o tempo no banco
    with mock_db_time(model=User) as time:
        # Cria usuário diretamente no ORM
        new_user = User(
            username='alice',
            password='secret',
            email='teste@test'
        )
        session.add(new_user)
        await session.commit()

    # Busca usuário no banco
    user = await session.scalar(
        select(User).where(User.username == 'alice')
    )

    # Converte para dict e compara tudo
    assert asdict(user) == {
        'id': 1,
        'username': 'alice',
        'password': 'secret',
        'email': 'teste@test',
        'created_at': time,  # tempo mockado
        'todos': [],  # sem tarefas
    }


# TESTE DE CRIAÇÃO DE TODO
@pytest.mark.asyncio
async def test_create_todo(session, user):
    # Cria tarefa vinculada ao usuário
    todo = Todo(
        title='Test Todo',
        description='Test Desc',
        state='draft',  # usando enum como string
        user_id=user.id,
    )

    session.add(todo)
    await session.commit()

    # Busca tarefa
    todo = await session.scalar(select(Todo))

    # Valida todos os campos
    assert asdict(todo) == {
        'description': 'Test Desc',
        'id': 1,
        'state': 'draft',
        'title': 'Test Todo',
        'user_id': 1,
    }


# TESTE DE RELACIONAMENTO
@pytest.mark.asyncio
async def test_user_todo_relationship(session, user: User):
    # Cria tarefa ligada ao usuário
    todo = Todo(
        title='Test Todo',
        description='Test Desc',
        state='draft',
        user_id=user.id,
    )

    session.add(todo)
    await session.commit()
    # Atualiza dados do usuário (importante!)
    await session.refresh(user)
    # Busca usuário novamente do banco
    user = await session.scalar(
        select(User).where(User.id == user.id)
    )
    # Verifica relacionamento 1:N
    assert user.todos == [todo]
