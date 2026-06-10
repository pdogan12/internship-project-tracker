from datetime import datetime
from rich.console import Console
from rich.table import Table
from . import store

console = Console()


def add_project(name: str, description: str) -> None:
    data = store.load()
    pid = store.new_id()
    data["projects"][pid] = {
        "id": pid,
        "name": name,
        "description": description,
        "created_at": datetime.now().isoformat(),
    }
    store.save(data)
    console.print(f"[green]Added project[/green] [bold]{name}[/bold] (id: {pid})")


def list_projects() -> None:
    data = store.load()
    if not data["projects"]:
        console.print("[dim]No projects yet. Use 'add-project' to create one.[/dim]")
        return

    table = Table(title="Projects", show_lines=True)
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("Name", style="bold")
    table.add_column("Description")
    table.add_column("Tasks", justify="right")

    for p in data["projects"].values():
        task_count = sum(
            1 for t in data["tasks"].values() if t["project_id"] == p["id"]
        )
        table.add_row(p["id"], p["name"], p.get("description", ""), str(task_count))

    console.print(table)
