from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import Literal


class Settings(BaseSettings):
    # App
    log_level: str = "INFO"
    cors_origins: list[str] = ["http://localhost:5173"]
    snapshot_interval_seconds: int = 30
    ws_heartbeat_seconds: int = 20

    # Database (required — set DATABASE_URL to your Neon connection string)
    database_url: str

    # Clerk
    clerk_jwks_url: str = ""
    clerk_issuer: str = ""
    clerk_audience: str = "ibkr-dashboard"
    clerk_secret_key: str = ""

    # IB Gateway
    ib_gateway_host: str = "localhost"
    ib_gateway_port: int = 4002
    ib_client_id: int = 17
    ib_account_id: str = ""
    trading_mode: Literal["paper", "live"] = "paper"

    # Anthropic
    anthropic_api_key: str = ""
    anthropic_model: str = "claude-opus-4-5"
    anthropic_max_tokens: int = 4096

    class Config:
        env_file = ".env"
        extra = "ignore"


@lru_cache
def get_settings() -> Settings:
    return Settings()
