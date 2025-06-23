from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "TechnicalServer"
    admin_email: str = "none@entropy.sc"
    database_url: str = "postgresql://user:password@host:port/db"
    
    debug: bool = True
    host: str = "localhost"
    port: int = 18080
    workers: int = 1
    prefix: str = "/api"
    public_address: str = "http://localhost:5173/"
    response_timeout: int = 300

    cors_allow_origins: str = "*"
    cors_allow_origin_regex: str = "*"
    cors_allow_methods: str = "*"
    cors_allow_headers: str = "*"
    cors_allow_credentials: bool = False

    model_config = SettingsConfigDict(env_file=".env")


@lru_cache
def get_settings():
    return Settings()


settings = get_settings()
