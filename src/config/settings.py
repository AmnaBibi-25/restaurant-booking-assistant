import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

def _resolve_path(value: str, base_level: int=2) -> Path:
    """
    Resolves relative paths against project root.
    Keeps absolute paths unchanged
    """

    path_obj = Path(value)
    if not path_obj.is_absolute():
        base_dir = Path(__file__).resolve().parents[base_level]
        path_obj = base_dir / path_obj

    return path_obj.resolve()

# Base Directory
BASE_DIR = Path(__file__).resolve().parents[2]

# Paths (relative or absolute)
MENUS_DIR = _resolve_path(os.getenv("MENUS_DIR", "data/menus"))
PERSIST_DIR = _resolve_path(os.getenv("PERSIST_DIR", "chroma_db"))

# Ensure required directories exist
PERSIST_DIR.mkdir(parents=True, exist_ok=True)