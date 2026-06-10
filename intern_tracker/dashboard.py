from datetime import date, datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich import box
from . import store
from .tasks import PRIORITY_COLORS

console = Console()

STATUS_ICONS = {"todo": "○", "in-progress": "◐", "done": "●"}
STATUS_COLORS = {"todo": "dim", "in-progress": "blue", "done": "green"}


def _task_row(task: dict, today: date) -> tuple[str, ...]:
    status = task["status"]
    icon = STATUS_ICONS[status]
    status_color = STATUS_COLORS[status]
    prio_color = PRIORITY_COLORS[task["priority"]]

    due_str = ""
    due_style = ""
    if task["due_date"]:
        due = date.fromisoformat(task["due_date"])
        days_left = (due - today).days
        if status != "done":
            if days_left < 0:
                due_style = "bold red"
                due_str = f"{task['due_date']} (!overdue)"
            elif days_left <= 3:
                due_style = "yellow"
                due_str = f"{task['due_date']} ({days_left}d)"
            else:
                due_str = task["due_date"]
        else:
            due_str = task["due_date"]

    return (icon, status_color, task["title"], prio_color, task["priority"], due_str, due_style)


def show_dashboard() -> None:
    data = store.load()
    today = date.today()

    if not data["projects"]:
        console.print(Panel("[dim]No projects yet. Run 'intern-tracker add-project' to start.[/dim]", title="Dashboard"))
        return

    overdue: list[dict] = []
    upcoming: list[dict] = []

    for project in data["projects"].values():
        tasks = [t for t in data["tasks"].values() if t["project_id"] == project["id"]]
        total = len(tasks)
        done = sum(1 for t in tasks if t["status"] == "done")

        progress_bar = _make_progress(done, total)
        header = Text()
        header.append(f"  {project['name']}", style="bold white")
        if project.get("description"):
            header.append(f"  —  {project['description']}", style="dim")
        header.append(f"  {progress_bar}  {done}/{total} tasks", style="dim")
        console.print(header)

        if not tasks:
            console.print("    [dim]No tasks.[/dim]")
            console.print()
            continue

        table = Table(box=box.SIMPLE, show_header=True, pad_edge=False, padding=(0, 1))
        table.add_column("", width=2)
        table.add_column("Task", style="white")
        table.add_column("Priority", width=8)
        table.add_column("Due", width=22)
        table.add_column("ID", style="dim", width=8)

        for task in sorted(tasks, key=lambda t: (t["status"] == "done", t["priority"] != "high")):
            icon, status_color, title, prio_color, prio, due_str, due_style = _task_row(task, today)

            title_text = Text(title, style=status_color)
            if task["status"] == "done":
                title_text.stylize("strike")

            prio_text = Text(prio, style=prio_color)
            due_text = Text(due_str, style=due_style) if due_style else Text(due_str)

            table.add_row(Text(icon, style=status_color), title_text, prio_text, due_text, Text(task["id"], style="dim"))

            if task["status"] != "done" and task["due_date"]:
                due = date.fromisoformat(task["due_date"])
                days_left = (due - today).days
                if days_left < 0:
                    overdue.append(task)
                elif days_left <= 3:
                    upcoming.append(task)

        console.print(table)
        console.print()

    if overdue or upcoming:
        summary = Text()
        if overdue:
            summary.append(f"  {len(overdue)} overdue", style="bold red")
        if overdue and upcoming:
            summary.append("  ·  ")
        if upcoming:
            summary.append(f"  {len(upcoming)} due within 3 days", style="yellow")
        console.print(Panel(summary, title="Alerts", border_style="red" if overdue else "yellow"))


def _make_progress(done: int, total: int) -> str:
    if total == 0:
        return "[ — ]"
    filled = round(done / total * 10)
    bar = "█" * filled + "░" * (10 - filled)
    return f"[{bar}]"
