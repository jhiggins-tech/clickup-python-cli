# ClickUp CLI

A CLI tool for interacting with the ClickUp API. Requires `CLICKUP_API_KEY` env var set to a personal API token (starts with `pk_`).

## Running

```bash
uvx --from git+https://github.com/jhiggins-tech/clickup-python-cli clickup <command>
```

## Hierarchy

workspaces → spaces → folders → lists → tasks

Start with `clickup workspaces` to get your team ID, then drill down through the hierarchy. Each command outputs the IDs needed for the next level.

## Commands

```bash
# List workspaces (returns TEAM_ID)
clickup workspaces

# List spaces in a workspace (returns SPACE_ID)
clickup spaces TEAM_ID

# List folders in a space (returns FOLDER_ID)
clickup folders SPACE_ID

# List lists in a folder (returns LIST_ID)
clickup lists FOLDER_ID

# List folderless lists directly in a space
clickup lists --space SPACE_ID

# List tasks in a list (100 per page)
clickup tasks LIST_ID
clickup tasks LIST_ID --page 1

# Show full task detail
clickup task TASK_ID

# Show items shared with you
clickup shared TEAM_ID

# Create a task
clickup create LIST_ID "Task name"
clickup create LIST_ID "Task name" -d "Description" -s "to do" -p 3
```

## Create task options

| Flag | Description |
|------|-------------|
| `-d` | Task description |
| `-s` | Task status (e.g. "to do", "in progress") |
| `-p` | Priority: 1=urgent, 2=high, 3=normal, 4=low |
