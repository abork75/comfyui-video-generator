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

    # ComfyUI (Linux – transitions, port 8189)
    comfyui_url: str = "http://127.0.0.1:8189"

    # ComfyUI Upscaler (Windows – RealESRGAN, port 8100)
    comfyui_upscale_url: str = "http://127.0.0.1:8100"
    comfyui_upscale_input_dir:  str = r"D:\ComfyUI\input"
    comfyui_upscale_output_dir: str = r"D:\ComfyUI\output"

    # Environment management
    wsl_distro: str = "Ubuntu"
    linux_comfyui_cmd: str = (
        "cd ~/ComfyUI && source venv/bin/activate && "
        "python main.py --listen 0.0.0.0 --port 8189 --disable-cuda-malloc"
    )
    windows_comfyui_exe: str = (
        r"C:\Users\abork\AppData\Local\Programs\ComfyUI\ComfyUI.exe"
    )

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
