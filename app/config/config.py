
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    prefix: str = "/api/v1"


settings = Settings()


