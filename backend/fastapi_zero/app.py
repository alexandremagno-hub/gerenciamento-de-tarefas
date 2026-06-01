import asyncio
import sys
from http import HTTPStatus
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from fastapi_zero.routers import auth, todos, users
from fastapi_zero.schemas import Message
from fastapi_zero.database import engine
from fastapi_zero.models import table_registry

# Windows fix
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# AQUI É ONDE CRIA AS TABELAS
@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(table_registry.metadata.create_all)
    yield

# PASSA O LIFESPAN AQUI
app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# rotas
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(todos.router)

@app.get(
    '/',
    status_code=HTTPStatus.OK,
    response_model=Message,
)
def read_root():
    return {'message': 'Olá Mundo!'}
