from datetime import datetime
from enum import Enum

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import (
    Mapped,
    mapped_as_dataclass,
    mapped_column,
    registry,
    relationship,
)

# Registro central das tabelas
table_registry = registry()


# Enum (estado da tarefa)
class TodoState(str, Enum):
    draft = 'draft'
    todo = 'todo'
    doing = 'doing'
    done = 'done'
    trash = 'trash'


# Tabela User
@mapped_as_dataclass(table_registry)
class User:
    __tablename__ = 'users'  # nome da tabela no banco

    # ID (chave primaria)
    id: Mapped[int] = mapped_column(
        init=False,  # não entra no contrutor
        primary_key=True
    )
    # Nome de usuário (único)
    username: Mapped[str] = mapped_column(unique=True)
    # Email (único)
    email: Mapped[str] = mapped_column(unique=True)
    # Senha (hash)
    password: Mapped[str]
    # Data de criação automatica
    created_at: Mapped[datetime] = mapped_column(
        init=False,
        server_default=func.now()  # NOW() no banco
    )
    # Relacionamento com todos (1 usuário -> várias tarefas)
    todos: Mapped[list['Todo']] = relationship(
        init=False,
        cascade='all, delete-orphan',  # deleta todos junto com usuário
        lazy='selectin',  # carregamento otimizado
    )


# Tabela Todo
@mapped_as_dataclass(table_registry)
class Todo:
    __tablename__ = 'todos'

    # ID da tarefa
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    # Título
    title: Mapped[str]
    # Descrição
    description: Mapped[str]
    # Estado  (usa ENUM)
    state: Mapped[TodoState]

    # Chave estrangeira (ligaçao com o usuário)
    user_id: Mapped[int] = mapped_column(
        ForeignKey('users.id')  # referência à tabela users
    )
