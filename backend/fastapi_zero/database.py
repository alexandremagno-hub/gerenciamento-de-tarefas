from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from fastapi_zero.settings import Settings

settings = Settings()

# engine global (ESSENCIAL)
engine = create_async_engine(settings.DATABASE_URL)

# fábrica de sessões (melhor prática)
SessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False
)

# 👇 dependência do FastAPI
async def get_session():  # pragma: no cover
    async with SessionLocal() as session:
        yield session
