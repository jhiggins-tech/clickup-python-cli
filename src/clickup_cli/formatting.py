import click


def format_workspaces(teams: list[dict]) -> None:
    for team in teams:
        click.echo(f"  {team['id']}  {team['name']}")


def format_spaces(spaces: list[dict]) -> None:
    for space in spaces:
        click.echo(f"  {space['id']}  {space['name']}")


def format_folders(folders: list[dict]) -> None:
    for folder in folders:
        click.echo(f"  {folder['id']}  {folder['name']}")


def format_lists(lists: list[dict]) -> None:
    for lst in lists:
        task_count = lst.get("task_count", "?")
        click.echo(f"  {lst['id']}  {lst['name']}  ({task_count} tasks)")


def format_tasks(tasks: list[dict]) -> None:
    for task in tasks:
        status = task.get("status", {}).get("status", "?")
        click.echo(f"  {task['id']}  [{status}]  {task['name']}")


def format_shared(shared: dict) -> None:
    folders = shared.get("folders", [])
    lists = shared.get("lists", [])
    tasks = shared.get("tasks", [])
    if folders:
        click.echo("Folders:")
        for f in folders:
            click.echo(f"  {f['id']}  {f['name']}")
    if lists:
        click.echo("Lists:")
        for lst in lists:
            click.echo(f"  {lst['id']}  {lst['name']}  ({lst.get('task_count', '?')} tasks)")
    if tasks:
        click.echo("Tasks:")
        for t in tasks:
            click.echo(f"  {t}")
    if not folders and not lists and not tasks:
        click.echo("  No shared items.")


def format_all_tasks(tasks: list[dict], *, limit: int = 0) -> None:
    """Print tasks from a workspace, grouped by their list."""
    if not tasks:
        click.echo("  No tasks found.")
        return
    current_list = None
    total = 0
    for task in tasks:
        if limit and total >= limit:
            return
        list_info = task.get("list", {})
        list_id = list_info.get("id", "?")
        list_name = list_info.get("name", "?")
        list_key = list_id
        if list_key != current_list:
            click.echo(f"\nList: {list_name} ({list_id})")
            current_list = list_key
        status = task.get("status", {}).get("status", "?")
        click.echo(f"  {task['id']}  [{status}]  {task['name']}")
        total += 1


def format_task_detail(task: dict) -> None:
    click.echo(f"Task:        {task['name']}")
    click.echo(f"ID:          {task['id']}")
    click.echo(f"Status:      {task.get('status', {}).get('status', '?')}")
    click.echo(f"Priority:    {(task.get('priority') or {}).get('priority', 'none')}")
    parent = task.get("parent")
    if parent:
        click.echo(f"Parent:      {parent}")
    assignees = task.get("assignees", [])
    names = ", ".join(a.get("username", a.get("email", "?")) for a in assignees)
    click.echo(f"Assignees:   {names or 'none'}")
    click.echo(f"URL:         {task.get('url', '')}")
    subtasks = task.get("subtasks", [])
    if subtasks:
        click.echo(f"Subtasks:    {len(subtasks)}")
        for st in subtasks:
            click.echo(f"  {st['id']}  {st['name']}")
    desc = task.get("description", "")
    if desc:
        click.echo(f"\n{desc[:500]}")
