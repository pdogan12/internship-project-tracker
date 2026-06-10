from datetime import date
from typing import Optional
from rich.console import Console
from . import store
from .tasks import _resolve_project

console = Console()


def log_progress(note: str, project_ref: Optional[str]) -> None:
    data = store.load()

    project_id = None
    project_name = None
    if project_ref:
        project = _resolve_project(data, project_ref)
        if project is None:
            return
        project_id = project["id"]
        project_name = project["name"]

    entry = {
        "id": store.new_id(),
        "date": date.today().isoformat(),
        "project_id": project_id,
        "note": note,
    }
    data["logs"].append(entry)
    store.save(data)

    label = f" for [cyan]{project_name}[/cyan]" if project_name else ""
    console.print(f"[green]Logged progress[/green]{label}: {note}")
