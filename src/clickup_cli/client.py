from __future__ import annotations

import os
from typing import Any

import click
import httpx

BASE_URL = "https://api.clickup.com/api/v2"


class ClickUpClient:
    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or os.environ.get("CLICKUP_API_KEY")
        if not self.api_key:
            click.echo("Error: CLICKUP_API_KEY environment variable is not set.", err=True)
            raise SystemExit(1)
        self._client = httpx.Client(
            base_url=BASE_URL,
            headers={"Authorization": self.api_key},
            timeout=30.0,
        )

    def _request(self, method: str, path: str, params: dict | None = None, json: dict | None = None) -> dict:
        try:
            response = self._client.request(method, path, params=params, json=json)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            click.echo(f"API error {e.response.status_code}: {e.response.text}", err=True)
            raise SystemExit(1)
        except httpx.ConnectError:
            click.echo("Error: could not connect to ClickUp API.", err=True)
            raise SystemExit(1)

    def _get(self, path: str, params: dict | None = None) -> dict:
        return self._request("GET", path, params=params)

    def _post(self, path: str, json: dict | None = None) -> dict:
        return self._request("POST", path, json=json)

    def get_workspaces(self) -> list[dict]:
        return self._get("/team")["teams"]

    def get_spaces(self, team_id: str) -> list[dict]:
        return self._get(f"/team/{team_id}/space")["spaces"]

    def get_folders(self, space_id: str) -> list[dict]:
        return self._get(f"/space/{space_id}/folder")["folders"]

    def get_lists(self, folder_id: str) -> list[dict]:
        return self._get(f"/folder/{folder_id}/list")["lists"]

    def get_folderless_lists(self, space_id: str) -> list[dict]:
        return self._get(f"/space/{space_id}/list")["lists"]

    def get_shared(self, team_id: str) -> dict:
        return self._get(f"/team/{team_id}/shared")["shared"]

    def get_tasks(self, list_id: str, page: int = 0, *, subtasks: bool = False, include_closed: bool = False) -> list[dict]:
        params: dict[str, Any] = {"page": page}
        if subtasks:
            params["subtasks"] = "true"
        if include_closed:
            params["include_closed"] = "true"
        return self._get(f"/list/{list_id}/task", params=params)["tasks"]

    def get_task(self, task_id: str, *, include_subtasks: bool = False) -> dict:
        params: dict[str, Any] = {}
        if include_subtasks:
            params["include_subtasks"] = "true"
        return self._get(f"/task/{task_id}", params=params or None)

    def get_subtasks(self, task_id: str) -> list[dict]:
        task = self.get_task(task_id, include_subtasks=True)
        return task.get("subtasks", [])

    def create_task(self, list_id: str, name: str, **kwargs: Any) -> dict:
        body = {"name": name, **kwargs}
        return self._post(f"/list/{list_id}/task", json=body)

    def create_subtask(self, list_id: str, parent_id: str, name: str, **kwargs: Any) -> dict:
        return self.create_task(list_id, name, parent=parent_id, **kwargs)

    def get_all_tasks(
        self,
        team_id: str,
        *,
        statuses: list[str] | None = None,
        assignees: list[str] | None = None,
        include_closed: bool = False,
        subtasks: bool = False,
    ) -> list[dict]:
        """Fetch filtered tasks across a workspace via GET /team/{team_id}/task.

        Automatically paginates through all pages (100 tasks per page).
        """
        all_tasks: list[dict] = []
        page = 0
        while True:
            params: dict[str, Any] = {"page": page}
            if include_closed:
                params["include_closed"] = "true"
            if subtasks:
                params["subtasks"] = "true"
            if statuses:
                for i, s in enumerate(statuses):
                    params[f"statuses[{i}]"] = s
            if assignees:
                for i, a in enumerate(assignees):
                    params[f"assignees[{i}]"] = a
            batch = self._get(f"/team/{team_id}/task", params=params).get("tasks", [])
            all_tasks.extend(batch)
            if len(batch) < 100:
                break
            page += 1
        return all_tasks
