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


def format_task_detail(task: dict) -> None:
    click.echo(f"Task:        {task['name']}")
    click.echo(f"ID:          {task['id']}")
    click.echo(f"Status:      {task.get('status', {}).get('status', '?')}")
    click.echo(f"Priority:    {(task.get('priority') or {}).get('priority', 'none')}")
    assignees = task.get("assignees", [])
    names = ", ".join(a.get("username", a.get("email", "?")) for a in assignees)
    click.echo(f"Assignees:   {names or 'none'}")
    click.echo(f"URL:         {task.get('url', '')}")
    desc = task.get("description", "")
    if desc:
        click.echo(f"\n{desc[:500]}")
