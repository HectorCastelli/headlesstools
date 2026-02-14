import os
import logging
from pathlib import Path

# Setup relative paths
SCRIPTS_DIR = Path(__file__).parent
REPO_ROOT = SCRIPTS_DIR.parent
PACKS_DIR = REPO_ROOT / "packs"
DIST_DIR = REPO_ROOT / "dist"


def setup_logging():
    """
    Configures standard logging to respect LOG_ENV
    """
    logging.basicConfig(
        level=os.getenv("LOG_LEVEL", "INFO"), format="%(levelname)s: %(message)s"
    )


def load_env():
    """
    Loads the .env file and overwrites the current os.environ
    """
    env_path = SCRIPTS_DIR / ".env"
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            if "=" in line and not line.startswith("#"):
                key, val = line.split("=", 1)
                os.environ[key.strip()] = val.strip().strip('"').strip("'")


# Immediately load the env and setup logging when imported
load_env()
setup_logging()
