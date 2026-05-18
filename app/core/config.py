# -*- coding: utf-8 -*-
"""
App configuration — reads from .env file
"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Auth
    app_user: str = "admin"
    app_password: str = "changeme"
    secret_key: str = "dev-secret-key-change-in-production"
    session_expire_hours: int = 24

    # Server
    host: str = "0.0.0.0"
    port: int = 8000

    # ComfyUI
    comfyui_url: str = "http://127.0.0.1:8189"

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
