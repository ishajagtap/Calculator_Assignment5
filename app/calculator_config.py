# app/calculator_config.py
import os
from pathlib import Path
from dotenv import load_dotenv
from .exceptions import ConfigError

load_dotenv()

def get_env(key: str, default=None):
    val = os.getenv(key, default)
    return val

def get_history_path() -> str:
    path = get_env("HISTORY_CSV_PATH", "data/history.csv")
    p = Path(path)
    if not p.parent.exists():
        # do not create; caller may want to validate, but ensure folder exists
        p.parent.mkdir(parents=True, exist_ok=True)
    return str(path)

def get_auto_save() -> bool:
    val = get_env("AUTO_SAVE", "True")
    if isinstance(val, str):
        val_low = val.lower()
        if val_low in {"true", "1", "yes"}:
            return True
        if val_low in {"false", "0", "no"}:
            return False
    raise ConfigError("AUTO_SAVE must be a boolean-like value.")