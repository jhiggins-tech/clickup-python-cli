# clickup-cli

A thin CLI wrapper for the [ClickUp API](https://developer.clickup.com/reference).

## Install

Requires Python 3.11+ and [UV](https://docs.astral.sh/uv/).

### Run directly with `uvx` (no install needed)

```bash
export CLICKUP_API_KEY=pk_your_token_here
uvx --from git+https://github.com/jhiggins-tech/clickup-python-cli clickup workspaces
```

### Local development

```bash
git clone https://github.com/jhiggins-tech/clickup-python-cli.git
cd clickup-python-cli
uv sync
```

Set your ClickUp personal API token (starts with `pk_`):

```bash
export CLICKUP_API_KEY=pk_your_token_here
```

## Usage

```bash
# List your workspaces
uv run clickup workspaces

# List spaces in a workspace
uv run clickup spaces TEAM_ID

# List folders in a space
uv run clickup folders SPACE_ID

# List lists in a folder
uv run clickup lists FOLDER_ID

# List folderless lists in a space
uv run clickup lists --space SPACE_ID

# List tasks in a list
uv run clickup tasks LIST_ID

# Show task detail
uv run clickup task TASK_ID

# Show shared items (tasks, lists, folders shared with you)
uv run clickup shared TEAM_ID

# Create a task
uv run clickup create LIST_ID "Task name"
uv run clickup create LIST_ID "Task name" -d "Description" -p 3 -s "to do"
```

Navigate the hierarchy: **workspaces** → **spaces** → **folders** → **lists** → **tasks**
