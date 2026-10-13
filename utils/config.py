## load and validate env configurations

import os
from pathlib import Path

from dotenv import load_dotenv

# Find the project root relative to this file.
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Load environment variables from the root .env file.
load_dotenv(PROJECT_ROOT / ".env")

def required_env(name: str) -> str:
    """Return a required environment variable or raise an error."""
    value = os.getenv(name)

    if not value:
        raise ValueError(
            f"Missing environment variable: {name}. "
            "Check your project-root .env file."
        )

    return value

# Model settings can be overridden through .env.
OPENAI_VISION_MODEL = os.getenv(
    "OPENAI_VISION_MODEL", "gpt-4o-mini"
)

OPENAI_TTS_MODEL = os.getenv(
    "OPENAI_TTS_MODEL", "gpt-4o-mini-tts"
)

OPENAI_TTS_VOICE = os.getenv(
    "OPENAI_TTS_VOICE", "coral"
)

# Resolve data directories relative to the project root.
UPLOAD_DIR = PROJECT_ROOT / os.getenv("UPLOAD_DIR", "uploads")
AUDIO_DIR = PROJECT_ROOT / os.getenv("AUDIO_DIR", "audio")

# Keep uploaded files within a configurable size limit.
MAX_UPLOAD_MB = int(os.getenv("MAX_UPLOAD_MB", "20"))

# Create directories if they do not exist.
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
AUDIO_DIR.mkdir(parents=True, exist_ok=True)
