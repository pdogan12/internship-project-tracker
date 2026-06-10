import json
import uuid
from datetime import datetime, date
from pathlib import Path
from typing import Any

DATA_FILE = Path.home() / ".intern-tracker" / "data.json"


def _default(obj: Any) -> str:
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")


def load() -> dict:
    if not DATA_FILE.exists():
        return {"projects": {}, "tasks": {}, "logs": []}
    with DATA_FILE.open() as f:
        return json.load(f)


def save(data: dict) -> None:
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    with DATA_FILE.open("w") as f:
        json.dump(data, f, indent=2, default=_default)


def new_id() -> str:
    return str(uuid.uuid4())[:8]
