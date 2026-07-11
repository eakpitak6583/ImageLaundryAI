from pathlib import Path
from dotenv import load_dotenv
import os

# ==========================================================
# Base Directory
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent

load_dotenv(BASE_DIR / ".env")


class Config:

    # ==========================================================
    # Flask
    # ==========================================================

    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "LaundryBotV7Enterprise"
    )

    DEBUG = os.getenv(
        "DEBUG",
        "False"
    ).lower() == "true"

    HOST = os.getenv(
        "HOST",
        "0.0.0.0"
    )

    PORT = int(
        os.getenv(
            "PORT",
            5000
        )
    )

    # ==========================================================
    # OpenAI
    # ==========================================================

    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

    MODEL_NAME = os.getenv(
        "OPENAI_MODEL",
        "gpt-5.5"
    )

    # ==========================================================
    # Database
    # ==========================================================

    DATABASE_PATH = BASE_DIR / "database" / "laundry.db"

    # ==========================================================
    # Project Folder
    # ==========================================================

    MANUAL_PATH = BASE_DIR / "manuals" / "pdf"

    REPAIR_PATH = BASE_DIR / "repair_reports"

    CACHE_FOLDER = BASE_DIR / "cache"

    LOG_FOLDER = BASE_DIR / "logs"

    PROMPT_FOLDER = BASE_DIR / "prompts"

    VECTOR_DB = BASE_DIR / "vector_db"
    PROMPT_FOLDER = BASE_DIR / "prompts"

    # ==========================================================
    # Upload
    # ==========================================================

    UPLOAD_FOLDER = BASE_DIR / "uploads"

    MACHINE_IMAGE_FOLDER = UPLOAD_FOLDER / "machine_images"

    MANUAL_UPLOAD_FOLDER = UPLOAD_FOLDER / "manuals"

    PART_UPLOAD_FOLDER = UPLOAD_FOLDER / "parts"

    # ==========================================================
    # Upload Limit
    # ==========================================================

    MAX_CONTENT_LENGTH = 30 * 1024 * 1024
    # ==========================================================
# Branding
# ==========================================================

SYSTEM_NAME = "Image Laundry AI"

SYSTEM_SUBTITLE = (
    "Computerized Maintenance Management System"
)

COMPANY_NAME = (
    "Accurate Technologies Co., Ltd."
)

SYSTEM_VERSION = "V1.0"