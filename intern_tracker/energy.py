from datetime import datetime
from rich.console import Console
from . import store

console = Console()

_LABELS = {1: "very low", 2: "low", 3: "okay", 4: "good", 5: "great"}
_COLORS = {1: "red", 2: "yellow", 3: "cyan", 4: "green", 5: "bold green"}


def log_energy(level: int) -> None:
    if not 1 <= level <= 5:
        console.print("[red]Energy level must be between 1 and 5.[/red]")
        return

    data = store.load()
    data["energy_logs"].append({
        "id": store.new_id(),
        "timestamp": datetime.now().isoformat(),
        "level": level,
    })
    store.save(data)

    bars = "█" * level + "░" * (5 - level)
    color = _COLORS[level]
    console.print(f"[{color}]Energy: {bars} {level}/5 — {_LABELS[level]}[/{color}]")
