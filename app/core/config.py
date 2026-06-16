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
    port: int = 8001

    # ComfyUI (Linux – transitions, port 8189)
    comfyui_url: str = "http://127.0.0.1:8189"

    # ComfyUI (Windows standalone, port 8000)
    comfyui_upscale_url: str = "http://127.0.0.1:8000"
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

    # Talk (InfiniteTalk) — Linux ComfyUI, port 8189
    # Linux ComfyUI (WSL2) mounts the Windows D: drive at /mnt/d, so input/output
    # are accessible from Windows via the regular D:\ paths (same as upscaler).
    comfyui_linux_input_dir:  str = r"D:\ComfyUI\input"
    comfyui_linux_output_dir: str = r"D:\ComfyUI\output"
    # API-format workflow JSON exported from ComfyUI (Dev mode → Save API Format)
    talk_workflow_json: str = (
        r"D:\streamlit_project\comfyui_integration\workflow_configs\talk_workflow_api.json"
    )

    # CapCut export — desktop projects folder
    # Default: %LOCALAPPDATA%\CapCut\User Data\Projects\com.lveditor.draft
    capcut_projects_dir: str = (
        r"D:\CapCut\User Data\Projects\com.lveditor.draft"
    )
    # CapCut TEMPLATE project folder — cloned for each export.
    # Kept inside the app repo so it's version-controlled and independent of
    # the CapCut installation path.  Add more sibling folders (TEMPLATE_9x16,
    # TEMPLATE_SHORTS, …) here in future.
    capcut_template_dir: str = (
        r"D:\streamlit_project\comfyui_integration\CapCut export\TEMPLATE"
    )

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
