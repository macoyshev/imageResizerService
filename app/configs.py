from pydantic import BaseSettings


class Settings(BaseSettings):
    redis_host: str = '0.0.0.0'
    redis_port: int = 6379
