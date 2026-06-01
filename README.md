# FastAPI Next Fullstack

Aplicação full-stack de gerenciamento de tarefas com FastAPI (backend) e Next.js (frontend).

## Stack

| Camada | Tecnologias |
|---|---|
| Backend | FastAPI, Python 3.11+, SQLAlchemy 2 (async), PostgreSQL, Alembic, JWT |
| Frontend | Next.js 16, React 19, TypeScript, Tailwind CSS 4 |
| Infra | Docker Compose |

## Funcionalidades

- Autenticação com JWT (login, refresh token, senhas com Argon2)
- CRUD de usuários com autorização
- CRUD de tarefas (todos) com filtros por título, descrição e estado
- Frontend com rotas protegidas e dashboard

## Como rodar

### Com Docker

```bash
docker compose up --build
```

- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- Docs da API: http://localhost:8000/docs

### Localmente (sem Docker)

**Backend:**
```bash
cd backend
cp .env.example .env   # preencha as variáveis
poetry install
poetry run task run
```

**Frontend:**
```bash
cd frontend
npm install
echo 'NEXT_PUBLIC_API_URL="http://localhost:8000"' > .env.local
npm run dev
```

## Variáveis de ambiente

Backend — copie `backend/.env.example` para `backend/.env` e preencha:

| Variável | Descrição |
|---|---|
| `DATABASE_URL` | URL de conexão com PostgreSQL |
| `SECRET_KEY` | Chave secreta para assinar JWT |
| `ALGORITHM` | Algoritmo JWT (ex: HS256) |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Expiração do token em minutos |

## Testes

```bash
cd backend
poetry run task test
```

## Endpoints principais

| Método | Rota | Descrição |
|---|---|---|
| POST | `/auth/token` | Login |
| POST | `/auth/refresh_token` | Renovar token |
| POST | `/users/` | Criar usuário |
| GET | `/users/` | Listar usuários |
| GET | `/todos/` | Listar tarefas |
| POST | `/todos/` | Criar tarefa |
