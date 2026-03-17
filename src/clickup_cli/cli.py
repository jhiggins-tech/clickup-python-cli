import click

from clickup_cli import formatting
from clickup_cli.client import ClickUpClient


@click.group()
@click.pass_context
def cli(ctx):
    """ClickUp CLI - interact with ClickUp from the terminal."""
    ctx.ensure_object(dict)
    ctx.obj["client"] = ClickUpClient()


@cli.command()
@click.pass_context
def workspaces(ctx):
    """List available workspaces."""
    teams = ctx.obj["client"].get_workspaces()
    formatting.format_workspaces(teams)


@cli.command()
@click.argument("team_id")
@click.pass_context
def spaces(ctx, team_id):
    """List spaces in a workspace."""
    items = ctx.obj["client"].get_spaces(team_id)
    formatting.format_spaces(items)


@cli.command()
@click.argument("space_id")
@click.pass_context
def folders(ctx, space_id):
    """List folders in a space."""
    items = ctx.obj["client"].get_folders(space_id)
    formatting.format_folders(items)


@cli.command()
@click.argument("folder_id", required=False)
@click.option("--space", "space_id", help="List folderless lists in a space.")
@click.pass_context
def lists(ctx, folder_id, space_id):
    """List lists in a folder, or folderless lists with --space."""
    client = ctx.obj["client"]
    if space_id:
        items = client.get_folderless_lists(space_id)
    elif folder_id:
        items = client.get_lists(folder_id)
    else:
        raise click.UsageError("Provide a FOLDER_ID or use --space SPACE_ID.")
    formatting.format_lists(items)


@cli.command()
@click.argument("list_id")
@click.option("--page", default=0, help="Page number (100 tasks per page).")
@click.pass_context
def tasks(ctx, list_id, page):
    """List tasks in a list."""
    items = ctx.obj["client"].get_tasks(list_id, page=page)
    formatting.format_tasks(items)


@cli.command()
@click.argument("team_id")
@click.pass_context
def shared(ctx, team_id):
    """Show shared tasks, lists, and folders."""
    data = ctx.obj["client"].get_shared(team_id)
    formatting.format_shared(data)


@cli.command()
@click.argument("task_id")
@click.pass_context
def task(ctx, task_id):
    """Show task detail."""
    t = ctx.obj["client"].get_task(task_id)
    formatting.format_task_detail(t)


@cli.command()
@click.argument("list_id")
@click.argument("name")
@click.option("--description", "-d", help="Task description.")
@click.option("--status", "-s", help="Task status.")
@click.option("--priority", "-p", type=int, help="Priority (1=urgent, 2=high, 3=normal, 4=low).")
@click.pass_context
def create(ctx, list_id, name, description, status, priority):
    """Create a new task in a list."""
    kwargs = {}
    if description:
        kwargs["description"] = description
    if status:
        kwargs["status"] = status
    if priority is not None:
        kwargs["priority"] = priority
    t = ctx.obj["client"].create_task(list_id, name, **kwargs)
    click.echo(f"Created: {t['id']}  {t['name']}")
    click.echo(f"URL:     {t.get('url', '')}")
