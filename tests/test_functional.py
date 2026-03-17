"""Functional tests that call the real ClickUp API (read-only).

Requires CLICKUP_API_KEY to be set. Tests walk the workspace hierarchy
top-down, discovering IDs as they go. Skips gracefully when a level
of the hierarchy is empty.
"""

import os

import pytest
from click.testing import CliRunner

from clickup_cli.cli import cli
from clickup_cli.client import ClickUpClient

# ---------------------------------------------------------------------------
# Skip the entire module if no API key is available
# ---------------------------------------------------------------------------
pytestmark = pytest.mark.skipif(
    not os.environ.get("CLICKUP_API_KEY"),
    reason="CLICKUP_API_KEY not set",
)


# ---------------------------------------------------------------------------
# Shared state – populated as tests walk the hierarchy
# ---------------------------------------------------------------------------
class _Discovered:
    """Simple namespace to pass IDs between tests."""

    team_id: str | None = None
    space_id: str | None = None
    folder_id: str | None = None
    list_id: str | None = None
    task_id: str | None = None


discovered = _Discovered()


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------
@pytest.fixture(scope="module")
def client() -> ClickUpClient:
    return ClickUpClient()


@pytest.fixture(scope="module")
def runner() -> CliRunner:
    return CliRunner()


# ---------------------------------------------------------------------------
# Client-level tests (walk the hierarchy)
# ---------------------------------------------------------------------------
class TestClientHierarchy:
    """Test the ClickUpClient methods against the real API."""

    def test_get_workspaces(self, client: ClickUpClient) -> None:
        teams = client.get_workspaces()
        assert isinstance(teams, list)
        assert len(teams) > 0, "Expected at least one workspace"
        team = teams[0]
        assert "id" in team
        assert "name" in team
        discovered.team_id = str(team["id"])

    def test_get_spaces(self, client: ClickUpClient) -> None:
        if not discovered.team_id:
            pytest.skip("No workspace discovered")
        spaces = client.get_spaces(discovered.team_id)
        assert isinstance(spaces, list)
        assert len(spaces) > 0, "Expected at least one space"
        space = spaces[0]
        assert "id" in space
        assert "name" in space
        discovered.space_id = str(space["id"])

    def test_get_folders(self, client: ClickUpClient) -> None:
        if not discovered.space_id:
            pytest.skip("No space discovered")
        folders = client.get_folders(discovered.space_id)
        assert isinstance(folders, list)
        # Folders may be empty – that's fine, just record if we found one
        if folders:
            assert "id" in folders[0]
            assert "name" in folders[0]
            discovered.folder_id = str(folders[0]["id"])

    def test_get_lists_in_folder(self, client: ClickUpClient) -> None:
        if not discovered.folder_id:
            pytest.skip("No folder discovered")
        lists = client.get_lists(discovered.folder_id)
        assert isinstance(lists, list)
        if lists:
            assert "id" in lists[0]
            assert "name" in lists[0]
            discovered.list_id = str(lists[0]["id"])

    def test_get_folderless_lists(self, client: ClickUpClient) -> None:
        if not discovered.space_id:
            pytest.skip("No space discovered")
        lists = client.get_folderless_lists(discovered.space_id)
        assert isinstance(lists, list)
        # If we still don't have a list_id, grab one from folderless lists
        if not discovered.list_id and lists:
            discovered.list_id = str(lists[0]["id"])

    def test_get_tasks(self, client: ClickUpClient) -> None:
        if not discovered.list_id:
            pytest.skip("No list discovered")
        tasks = client.get_tasks(discovered.list_id)
        assert isinstance(tasks, list)
        if tasks:
            task = tasks[0]
            assert "id" in task
            assert "name" in task
            discovered.task_id = str(task["id"])

    def test_get_task_detail(self, client: ClickUpClient) -> None:
        if not discovered.task_id:
            pytest.skip("No task discovered")
        task = client.get_task(discovered.task_id)
        assert isinstance(task, dict)
        assert task["id"] == discovered.task_id
        assert "name" in task
        assert "status" in task
        assert "url" in task


# ---------------------------------------------------------------------------
# CLI-level tests (via Click's CliRunner)
# ---------------------------------------------------------------------------
class TestCLICommands:
    """Test CLI commands produce successful output."""

    def test_workspaces_command(self, runner: CliRunner) -> None:
        result = runner.invoke(cli, ["workspaces"])
        assert result.exit_code == 0, result.output
        assert len(result.output.strip()) > 0

    def test_spaces_command(self, runner: CliRunner) -> None:
        if not discovered.team_id:
            pytest.skip("No workspace discovered")
        result = runner.invoke(cli, ["spaces", discovered.team_id])
        assert result.exit_code == 0, result.output

    def test_folders_command(self, runner: CliRunner) -> None:
        if not discovered.space_id:
            pytest.skip("No space discovered")
        result = runner.invoke(cli, ["folders", discovered.space_id])
        assert result.exit_code == 0, result.output

    def test_lists_folder_command(self, runner: CliRunner) -> None:
        if not discovered.folder_id:
            pytest.skip("No folder discovered")
        result = runner.invoke(cli, ["lists", discovered.folder_id])
        assert result.exit_code == 0, result.output

    def test_lists_space_command(self, runner: CliRunner) -> None:
        if not discovered.space_id:
            pytest.skip("No space discovered")
        result = runner.invoke(cli, ["lists", "--space", discovered.space_id])
        assert result.exit_code == 0, result.output

    def test_tasks_command(self, runner: CliRunner) -> None:
        if not discovered.list_id:
            pytest.skip("No list discovered")
        result = runner.invoke(cli, ["tasks", discovered.list_id])
        assert result.exit_code == 0, result.output

    def test_task_command(self, runner: CliRunner) -> None:
        if not discovered.task_id:
            pytest.skip("No task discovered")
        result = runner.invoke(cli, ["task", discovered.task_id])
        assert result.exit_code == 0, result.output
        assert "Task:" in result.output
        assert "ID:" in result.output

    def test_shared_command(self, runner: CliRunner) -> None:
        if not discovered.team_id:
            pytest.skip("No workspace discovered")
        result = runner.invoke(cli, ["shared", discovered.team_id])
        assert result.exit_code == 0, result.output
