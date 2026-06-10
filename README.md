# intern-tracker

A CLI tool for managing internship projects and tasks. Data is stored in `~/.intern-tracker/data.json`.

## Installation

```bash
uv tool install .
```

Or run without installing:

```bash
uv run intern-tracker <command>
```

## Commands

### Projects

```bash
# Add a project
intern-tracker add-project "Backend API" -d "REST API for the intern portal"
```

### Tasks

```bash
# Add a task to a project (project can be id or partial name)
intern-tracker add-task Backend "Design database schema" --due 2026-06-15 -p high
intern-tracker add-task Backend "Write tests" -p medium

# Update task status: todo | in-progress | done
intern-tracker update-task "Design database" done
intern-tracker update-task <task-id> in-progress
```

### Progress Logs

```bash
# Log a daily note (optionally tied to a project)
intern-tracker log "Finished the auth middleware" -p Backend
intern-tracker log "Reviewed PRs today"
```

### Views

```bash
# Dashboard: all projects and tasks, overdue tasks in red, due-soon in yellow
intern-tracker dashboard

# Weekly standup: done, in-progress, up next, and recent notes
intern-tracker standup
```

## Priority levels

`high` (red) · `medium` (yellow, default) · `low` (green)

## Task statuses

`todo` · `in-progress` · `done`

### Focus Sessions

```bash
# Start a focus session (will prompt for what you're working on)
intern-tracker session start

# Check current session status + elapsed time
intern-tracker session status

# End focus session and start a break (recommends break length)
intern-tracker session break

# End your break, ready for next session
intern-tracker session end
```

### Energy Tracking

```bash
# Log your current energy level (1=very low, 5=great)
intern-tracker energy log 4
```

The dashboard includes a **Today's Rhythm** panel showing total focus time, number of sessions, and work/break ratio. It turns red and warns you if you've been in a focus session for 90+ minutes without a break.
