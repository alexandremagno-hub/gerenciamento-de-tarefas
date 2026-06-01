from pydantic import BaseModel, ConfigDict, EmailStr, Field

from fastapi_zero.models import TodoState


# Resposta simples
class Message(BaseModel):
    message: str


# Entrada de usuário (creat/update)
class UserSchema(BaseModel):
    username: str
    email: EmailStr  # valida automaticamente formato de email
    password: str


# Saída de usuário sem senha
class UserPublic(BaseModel):
    id: int
    username: str
    email: EmailStr
    # Permite converter de ORM (SQLAlchemy) para schema
    model_config = ConfigDict(from_attributes=True)


# Lista de usuários
class UserList(BaseModel):
    users: list[UserPublic]


# Token JWT (Resposta)
class Token(BaseModel):
    access_token: str  # token gerado
    token_type: str  # geralmente "Bearer"


# Paginação base
class FilterPage(BaseModel):
    offset: int = Field(ge=0, default=0)  # começao do registro x
    limit: int = Field(ge=0, default=10)  # quantidade de registro


# Criação de Todo
class TodoSchema(BaseModel):
    title: str
    description: str
    state: TodoState  # usa enum (validação automática)


# Saída de Todo
class TodoPublic(TodoSchema):
    id: int


# Lista de Todos
class TodoList(BaseModel):
    todos: list[TodoPublic]


# Filtro + Paginação
class FilterTodo(FilterPage):
    # Campos opcionais para busca
    title: str | None = Field(None, min_length=3, max_length=20)
    description: str | None = Field(None, min_length=3, max_length=20)
    state: TodoState | None = None


# Atualização parcial
class TodoUpdate(BaseModel):
    # Todos opcionais → permite atualizar parcialmente
    title: str | None = None
    description: str | None = None
    state: TodoState | None = None
