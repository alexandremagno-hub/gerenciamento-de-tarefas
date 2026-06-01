from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


# Classe de configuração da aplicação
class Settings(BaseSettings):
    model_config = SettingsConfigDict(  # configuração do pydantic
        env_file='.env',  # lê arquivo .env
        env_file_encoding='utf-8'  # usa codificação UTF-8
    )

    # URL do banco de dados
    DATABASE_URL: str = Field(init=False)
    # Chave secreta usada para assinar JWT
    SECRET_KEY: str = Field(init=False)
    # Algoritmo do JWT
    ALGORITHM: str = Field(init=False)
    # Tempo de expiração do token em minutos
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(init=False)
