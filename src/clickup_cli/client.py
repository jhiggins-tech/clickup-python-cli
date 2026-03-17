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

    def get_tasks(self, list_id: str, page: int = 0) -> list[dict]:
        return self._get(f"/list/{list_id}/task", params={"page": page})["tasks"]

    def get_task(self, task_id: str) -> dict:
        return self._get(f"/task/{task_id}")

    def create_task(self, list_id: str, name: str, **kwargs: Any) -> dict:
        body = {"name": name, **kwargs}
        return self._post(f"/list/{list_id}/task", json=body)
