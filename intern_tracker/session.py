from datetime import datetime
from typing import Optional
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from . import store

console = Console()


def _now() -> str:
    return datetime.now().isoformat()


def _duration_minutes(start_iso: str, end_iso: Optional[str] = None) -> float:
    start = datetime.fromisoformat(start_iso)
    end = datetime.fromisoformat(end_iso) if end_iso else datetime.now()
    return (end - start).total_seconds() / 60


def _active_session(data: dict, session_type: Optional[str] = None) -> Optional[dict]:
    for s in reversed(data["sessions"]):
        if s["end"] is None:
            if session_type is None or s["type"] == session_type:
                return s
    return None


def _break_recommendation(worked_minutes: float) -> int:
    if worked_minutes >= 90:
        return 20
    if worked_minutes >= 50:
        return 10
    return 5


def session_start(goal: Optional[str]) -> None:
    data = store.load()

    active = _active_session(data)
    if active is not None:
        console.print(
            f"[yellow]Already in a {active['type']} session.[/yellow] "
            "End it first with 'session break' or 'session end'."
        )
        return

    data["sessions"].append({
        "id": store.new_id(),
        "type": "focus",
        "start": _now(),
        "end": None,
        "goal": goal,
    })
    store.save(data)

    goal_str = f": [cyan]{goal}[/cyan]" if goal else ""
    console.print(f"[green]Focus session started[/green]{goal_str}")
    console.print("[dim]Run 'intern-tracker session break' when you need a break.[/dim]")


def session_break() -> None:
    data = store.load()

    active = _active_session(data, "focus")
    if active is None:
        console.print("[red]No active focus session.[/red] Start one with 'intern-tracker session start'.")
        return

    now = _now()
    worked = _duration_minutes(active["start"], now)
    active["end"] = now

    rec = _break_recommendation(worked)
    data["sessions"].append({
        "id": store.new_id(),
        "type": "break",
        "start": now,
        "end": None,
        "goal": None,
    })
    store.save(data)

    console.print(f"[blue]Break started[/blue] after [bold]{int(worked)}m[/bold] of focus.")
    console.print(f"[dim]Recommended break: {rec} minutes. Run 'intern-tracker session end' when done.[/dim]")


def session_end() -> None:
    data = store.load()

    active = _active_session(data, "break")
    if active is None:
        console.print("[red]No active break.[/red] Start a focus session first.")
        return

    now = _now()
    break_dur = _duration_minutes(active["start"], now)
    active["end"] = now
    store.save(data)

    console.print(f"[green]Break ended[/green] after {int(break_dur)}m. Ready for your next focus session!")
    console.print("[dim]Run 'intern-tracker session start' to begin.[/dim]")


def session_status() -> None:
    data = store.load()

    active = _active_session(data)
    if active is None:
        console.print("[dim]No active session. Run 'intern-tracker session start' to begin.[/dim]")
        return

    elapsed = int(_duration_minutes(active["start"]))
    if active["type"] == "focus":
        goal_str = f"  Goal: [cyan]{active['goal']}[/cyan]" if active["goal"] else ""
        console.print(f"[bold green]Focus session[/bold green] — {elapsed}m elapsed{goal_str}")
        if elapsed >= 90:
            console.print("[bold red]You've been focused for 90+ minutes — take a break![/bold red]")
    else:
        console.print(f"[bold blue]Break[/bold blue] — {elapsed}m elapsed")
