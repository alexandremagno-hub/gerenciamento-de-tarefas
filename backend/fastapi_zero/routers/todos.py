from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_zero.database import get_session
from fastapi_zero.models import Todo, User
from fastapi_zero.schemas import (
    FilterTodo,
    Message,
    TodoList,
    TodoPublic,
    TodoSchema,
    TodoUpdate,
)
from fastapi_zero.security import get_current_user

router = APIRouter()

# Sessão do banco
Session = Annotated[AsyncSession, Depends(get_session)]
# Usuário autenticado
CurrentUser = Annotated[User, Depends(get_current_user)]

# Router com prefixo
router = APIRouter(prefix='/todos', tags=['todos'])


# Cria Todo
@router.post(
    '/',
    response_model=TodoPublic,
)
async def create_todo(
    todo: TodoSchema,  # dodos enviados
    user: CurrentUser,  # usuário logado
    session: Session,
):
    # Cria objeto no banco vinculado ao usuário
    db_todo = Todo(
        title=todo.title,
        description=todo.description,
        state=todo.state,
        user_id=user.id,  # vínculo com usuário
    )
    session.add(db_todo)
    await session.commit()
    await session.refresh(db_todo)

    return db_todo


# Lista Todos
@router.get(
    '/',
    response_model=TodoList,
)
async def list_todos(
    session: Session,
    user: CurrentUser,
    todo_filter: Annotated[FilterTodo, Query()],
):
    # Base: só traz tarefas do usuário logado
    query = select(Todo).where(Todo.user_id == user.id)

    # Filtro por título
    if todo_filter.title:
        query = query.filter(Todo.title.contains(todo_filter.title))

    # Filtro por descrisão
    if todo_filter.description:
        query = query.filter(Todo.description.contains(todo_filter.description))

    # Filtro por estado
    if todo_filter.state:
        query = query.filter(Todo.state == todo_filter.state)

    # Paginação
    todos = await session.scalars(query.offset(todo_filter.offset).limit(todo_filter.limit))

    return {'todos': todos.all()}


# Atualização parcial
@router.patch(
    '/{todo_id}',
    response_model=TodoPublic,
)
async def patch_todo(
    todo_id: int,
    session: Session,
    user: CurrentUser,
    todo: TodoUpdate,  # pode enviar só alguns campos
):
    # Busca tarefa do usuário
    db_todo = await session.scalar(
        select(Todo).where(Todo.user_id == user.id, Todo.id == todo_id)
    )

    # Se não encontrar
    if not db_todo:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Task not found.'
        )

    # Atualiza apenas campos enviados
    for key, value in todo.model_dump(exclude_unset=True).items():
        setattr(db_todo, key, value)

    session.add(db_todo)
    await session.commit()
    await session.refresh(db_todo)

    return db_todo


# Deleta Todo
@router.delete(
    '/{todo_id}',
    response_model=Message,
)
async def delete_todo(
    todo_id: int,
    session: Session,
    user: CurrentUser,
):
    # Busca tarefa do usuário
    todo = await session.scalar(
        select(Todo).where(Todo.user_id == user.id, Todo.id == todo_id)
    )

    # Se não encontrar
    if not todo:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Task not found.')

    # Remove do banco
    await session.delete(todo)
    await session.commit()

    return {'message': 'Task has been deleted successfully.'}
