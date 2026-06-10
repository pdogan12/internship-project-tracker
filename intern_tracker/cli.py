import click
from . import projects, tasks, logs, dashboard, standup


@click.group()
@click.version_option("0.1.0", prog_name="intern-tracker")
def main():
    """Internship project and task tracker."""


# ── Projects ────────────────────────────────────────────────────────────────


@main.command("add-project")
@click.argument("name")
@click.option("-d", "--description", default="", help="Short description of the project.")
def add_project(name: str, description: str) -> None:
    """Add a new project."""
    projects.add_project(name, description)


# ── Tasks ────────────────────────────────────────────────────────────────────


@main.command("add-task")
@click.argument("project")
@click.argument("title")
@click.option(
    "--due",
    "due_date",
    default=None,
    metavar="YYYY-MM-DD",
    help="Due date for the task.",
)
@click.option(
    "-p",
    "--priority",
    type=click.Choice(["high", "medium", "low"], case_sensitive=False),
    default="medium",
    show_default=True,
    help="Task priority.",
)
def add_task(project: str, title: str, due_date: str, priority: str) -> None:
    """Add a task to PROJECT.

    PROJECT can be a project id or a partial name match.
    """
    tasks.add_task(project, title, due_date, priority.lower())


@main.command("update-task")
@click.argument("task")
@click.argument("status", type=click.Choice(["todo", "in-progress", "done"], case_sensitive=False))
def update_task(task: str, status: str) -> None:
    """Update a task's status.

    TASK can be a task id or a partial title match.
    """
    tasks.update_task_status(task, status.lower())


# ── Logs ─────────────────────────────────────────────────────────────────────


@main.command("log")
@click.argument("note")
@click.option(
    "-p",
    "--project",
    "project_ref",
    default=None,
    help="Associate this note with a project (id or name).",
)
def log_progress(note: str, project_ref: str) -> None:
    """Log a daily progress note."""
    logs.log_progress(note, project_ref)


# ── Views ─────────────────────────────────────────────────────────────────────


@main.command("dashboard")
def show_dashboard() -> None:
    """Show all projects and tasks, highlighting overdue and upcoming."""
    dashboard.show_dashboard()


@main.command("standup")
def show_standup() -> None:
    """Print a weekly standup summary (done, in-progress, up next)."""
    standup.print_standup()
