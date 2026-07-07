from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session

class Settings(BaseSettings):
    DATABASE_URL: str                                    # lida do .env
    model_config = SettingsConfigDict(env_file='.env')

settings = Settings()
engine = create_engine(settings.DATABASE_URL)            # conexão com o Supabase

class Base(DeclarativeBase):                             # base dos modelos ORM
    pass

def get_session():                                      # injeta a sessão nas rotas
    with Session(engine) as session:
        yield session