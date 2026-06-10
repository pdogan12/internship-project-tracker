from datetime import datetime, date
from typing import Optional
from rich.console import Console
from . import store

console = Console()

PRIORITIES = ("high", "medium", "low")
PRIORITY_COLORS = {"high": "red", "medium": "yellow", "low": "green"}
STATUSES = ("todo", "in-progress", "done")


def _resolve_project(data: dict, project_ref: str) -> Optional[dict]:
    """Find a project by id or name (case-insensitive partial match)."""
    if project_ref in data["projects"]:
        return data["projects"][project_ref]
    matches = [
        p for p in data["projects"].values()
        if project_ref.lower() in p["name"].lower()
    ]
    if len(matches) == 1:
        return matches[0]
    if len(matches) > 1:
        names = ", ".join(m["name"] for m in matches)
        console.print(f"[yellow]Ambiguous project '{project_ref}': {names}[/yellow]")
        return None
    console.print(f"[red]Project not found: '{project_ref}'[/red]")
    return None


def add_task(
    project_ref: str,
    title: str,
    due_date: Optional[str],
    priority: str,
) -> None:
    data = store.load()
    project = _resolve_project(data, project_ref)
    if project is None:
        return

    due = None
    if due_date:
        try:
            due = date.fromisoformat(due_date).isoformat()
        except ValueError:
            console.print(f"[red]Invalid date '{due_date}'. Use YYYY-MM-DD format.[/red]")
            return

    tid = store.new_id()
    data["tasks"][tid] = {
        "id": tid,
        "project_id": project["id"],
        "title": title,
        "due_date": due,
        "priority": priority,
        "status": "todo",
        "created_at": datetime.now().isoformat(),
        "completed_at": None,
    }
    store.save(data)
    prio_color = PRIORITY_COLORS[priority]
    console.print(
        f"[green]Added task[/green] [bold]{title}[/bold] "
        f"to [cyan]{project['name']}[/cyan] "
        f"([{prio_color}]{priority}[/{prio_color}]"
        + (f", due {due}" if due else "")
        + f") (id: {tid})"
    )


def update_task_status(task_ref: str, status: str) -> None:
    if status not in STATUSES:
        console.print(f"[red]Status must be one of: {', '.join(STATUSES)}[/red]")
        return

    data = store.load()
    task = data["tasks"].get(task_ref)
    if task is None:
        matches = [t for t in data["tasks"].values() if task_ref.lower() in t["title"].lower()]
        if len(matches) == 1:
            task = matches[0]
        elif len(matches) > 1:
            titles = ", ".join(m["title"] for m in matches)
            console.print(f"[yellow]Ambiguous task '{task_ref}': {titles}[/yellow]")
            return
        else:
            console.print(f"[red]Task not found: '{task_ref}'[/red]")
            return

    task["status"] = status
    if status == "done":
        task["completed_at"] = datetime.now().isoformat()
    else:
        task["completed_at"] = None
    store.save(data)
    console.print(f"[green]Task '{task['title']}' marked as {status}[/green]")
