from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # usually here should be some sort of a secret, but since it is test project i'll just let it be
    DATABASE_URL: str = "postgresql://user:password@localhost/example_db"

    class Config:
        env_file = ".env"

settings = Settings()
