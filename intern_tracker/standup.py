from datetime import date, timedelta
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from . import store

console = Console()


def print_standup() -> None:
    data = store.load()
    today = date.today()
    week_ago = today - timedelta(days=7)

    projects = data["projects"]

    # Completed this week
    completed = [
        t for t in data["tasks"].values()
        if t["status"] == "done"
        and t.get("completed_at")
        and date.fromisoformat(t["completed_at"][:10]) >= week_ago
    ]

    # In progress right now
    in_progress = [t for t in data["tasks"].values() if t["status"] == "in-progress"]

    # Todo tasks, sorted by priority then due date
    todo = [t for t in data["tasks"].values() if t["status"] == "todo"]
    priority_order = {"high": 0, "medium": 1, "low": 2}
    todo.sort(key=lambda t: (priority_order[t["priority"]], t.get("due_date") or "9999"))

    # Logs from the past week
    week_logs = [
        e for e in data["logs"]
        if date.fromisoformat(e["date"]) >= week_ago
    ]

    title = f"Weekly Standup  ·  {week_ago.isoformat()} → {today.isoformat()}"
    lines: list[Text] = []

    def section(heading: str) -> None:
        t = Text()
        t.append(f"\n{heading}\n", style="bold underline")
        lines.append(t)

    def bullet(text: str, style: str = "") -> None:
        t = Text()
        t.append("  • ", style="dim")
        t.append(text, style=style)
        t.append("\n")
        lines.append(t)

    def _project_name(task: dict) -> str:
        p = projects.get(task["project_id"])
        return p["name"] if p else "unknown"

    # ── Done ────────────────────────────────────────────────────────────
    section("Done")
    if completed:
        for t in completed:
            bullet(f"{t['title']}  [{_project_name(t)}]", style="green")
    else:
        bullet("Nothing completed this week.", style="dim")

    # ── In Progress ─────────────────────────────────────────────────────
    section("In Progress")
    if in_progress:
        for t in in_progress:
            due_note = f"  due {t['due_date']}" if t.get("due_date") else ""
            bullet(f"{t['title']}  [{_project_name(t)}]{due_note}", style="blue")
    else:
        bullet("Nothing in progress.", style="dim")

    # ── Up Next ─────────────────────────────────────────────────────────
    section("Up Next")
    upcoming = todo[:5]
    if upcoming:
        from .tasks import PRIORITY_COLORS
        for t in upcoming:
            color = PRIORITY_COLORS[t["priority"]]
            due_note = f"  due {t['due_date']}" if t.get("due_date") else ""
            bullet(f"{t['title']}  [{_project_name(t)}]{due_note}", style=color)
        if len(todo) > 5:
            bullet(f"…and {len(todo) - 5} more todo tasks", style="dim")
    else:
        bullet("No pending tasks.", style="dim")

    # ── Progress Notes ──────────────────────────────────────────────────
    if week_logs:
        section("Progress Notes")
        for entry in week_logs:
            proj = projects.get(entry["project_id"] or "")
            tag = f" [{proj['name']}]" if proj else ""
            bullet(f"{entry['date']}{tag}: {entry['note']}", style="dim")

    # ── Render ──────────────────────────────────────────────────────────
    combined = Text()
    for t in lines:
        combined.append_text(t)

    console.print(Panel(combined, title=title, border_style="cyan"))
