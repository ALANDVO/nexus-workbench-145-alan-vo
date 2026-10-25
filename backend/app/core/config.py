from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "Nexus Workbench"
    environment: str = "development"
    debug: bool = True

    cors_origins: List[str] = ["http://127.0.0.1:5173", "http://localhost:5173"]

    database_url: str = "sqlite+aiosqlite:///./nexus.db"

    keycloak_server_url: str = "http://127.0.0.1:8080"
    keycloak_realm: str = "nexus"
    keycloak_client_id: str = "nexus-workbench"
    keycloak_client_secret: str = ""

    github_token: str = ""
    github_repo: str = "anthropics/knowledge-work-plugins"


settings = Settings()