import os
import tempfile

# Vor dem Import des Servers setzen: Token-Cache und FIT-Downloads in ein Temp-Verzeichnis
os.environ.setdefault("GARMIN_MCP_DATA_DIR", tempfile.mkdtemp(prefix="garmin-mcp-test-"))

import pytest  # noqa: E402
from garmin_personal_api.errors import HttpError  # noqa: E402

from mcp_server_garmin_connect import server  # noqa: E402


class FakeAuth:
    def __init__(self) -> None:
        self.forced = 0
        self.fail_with: Exception | None = None

    def obtain_token(self, key: str, force_refresh: bool = False):
        if self.fail_with:
            raise self.fail_with
        self.forced += int(force_refresh)
        return type("Token", (), {"access_token": f"token-for-{key}"})()


class Seq:
    """Antwortfolge für aufeinanderfolgende Aufrufe; Exceptions werden geworfen."""

    def __init__(self, *items: object) -> None:
        self.items = list(items)

    def next(self) -> object:
        item = self.items.pop(0)
        if isinstance(item, Exception):
            raise item
        return item


class FakeClient:
    """Simuliert GarminPersonalApiClient; Antworten pro Methode setzbar."""

    def __init__(self) -> None:
        self.responses: dict[str, object] = {}
        self.calls: list[tuple[str, tuple, dict]] = []
        self.token = None

    def update_bearer_token(self, token: str) -> None:
        self.token = token

    def __getattr__(self, name: str):
        def call(*args, **kwargs):
            self.calls.append((name, args, kwargs))
            value = self.responses[name]
            if isinstance(value, Seq):
                return value.next()
            if isinstance(value, Exception):
                raise value
            return value() if callable(value) else value

        return call


def http_error(status: int, method: str = "GET") -> HttpError:
    return HttpError(status_code=status, method=method, url="https://example.invalid", response_text="x")


@pytest.fixture
def garmin(monkeypatch):
    monkeypatch.setenv("GARMIN_PERSONAL_API_KEY", "test-key")
    auth, client = FakeAuth(), FakeClient()
    monkeypatch.setattr(server.garmin, "_auth", auth)
    monkeypatch.setattr(server.garmin, "_client", client)
    return auth, client
