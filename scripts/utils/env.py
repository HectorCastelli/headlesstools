import os
from .paths import SCRIPTS_DIR


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


def is_debug():
    # Get the variable and normalize it to lowercase
    debug_val = os.environ.get("DEBUG", "").lower()

    if debug_val and debug_val != "false" and debug_val != "0":
        return True
    else:
        return False
