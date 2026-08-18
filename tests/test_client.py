"""Unit tests for PepkioClient with mocked HTTP responses."""

import httpx
import pytest

from pepkio_figure_panel_mockup_grid import (
    DEFAULT_API_BASE_URL,
    TOOL_ID,
    PepkioAPIError,
    PepkioAuthError,
    PepkioClient,
)


def test_client_init_defaults():
    client = PepkioClient(api_key="test-key")
    assert client.base_url == DEFAULT_API_BASE_URL
    assert client.api_key == "test-key"


def test_client_init_custom_base_url():
    client = PepkioClient(api_key="test-key", base_url="https://tools.localtest.me/")
    assert client.base_url == "https://tools.localtest.me"


def test_get_manifest_success():
    mock_manifest = {
        "schema_version": "1.0",
        "tool_id": TOOL_ID,
        "title": "Figure Panel Mockup Grid",
        "description": "Plan scientific figure layouts",
        "tags": ["figure"],
        "category": "lab-operations",
        "execution_mode": "sync",
        "estimated_runtime_sec": 1,
        "input": {"type": "object"},
        "output": {"type": "object"},
        "examples": [{"name": "scaffold_2x3", "input": {"action": "scaffold"}, "output": {}}],
    }

    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == f"/api/tools/v1/tools/{TOOL_ID}/manifest"
        assert request.method == "GET"
        return httpx.Response(200, json=mock_manifest)

    transport = httpx.MockTransport(handler)
    client = PepkioClient(api_key="test-key")
    client._client = httpx.Client(transport=transport, base_url=DEFAULT_API_BASE_URL)

    manifest = client.get_manifest()
    assert manifest["tool_id"] == TOOL_ID
    assert manifest["title"] == "Figure Panel Mockup Grid"


def test_run_success():
    mock_run_response = {
        "run_id": "test-run-123",
        "status": "completed",
        "result": {
            "document": {
                "journal": "nature",
                "columnWidth": "2-col",
                "panels": [{"id": "p1", "x": 0, "y": 0, "width": 50, "height": 40}],
            }
        },
        "error": None,
        "duration_ms": 5,
        "result_url": "https://tools.pepkio.com/api/tools/v1/runs/test-run-123",
        "permalink": "https://tools.pepkio.com/r/test-run-123",
    }

    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == f"/api/tools/v1/tools/{TOOL_ID}/run"
        assert request.method == "POST"
        assert request.headers["authorization"] == "Bearer test-key"
        payload = request.read().decode("utf-8")
        assert "scaffold" in payload
        return httpx.Response(200, json=mock_run_response)

    transport = httpx.MockTransport(handler)
    client = PepkioClient(api_key="test-key")
    client._client = httpx.Client(transport=transport, base_url=DEFAULT_API_BASE_URL)

    res = client.run(input={"action": "scaffold", "rows": 2, "cols": 3})
    assert res.run_id == "test-run-123"
    assert res.status == "completed"
    assert res.result["document"]["journal"] == "nature"


def test_run_missing_api_key(monkeypatch):
    monkeypatch.delenv("PEPKIO_API_KEY", raising=False)
    monkeypatch.delenv("LOCAL_PEPKIO_API_KEY", raising=False)
    client = PepkioClient(api_key=None, base_url="https://tools.pepkio.com")
    with pytest.raises(PepkioAuthError, match="API key is required"):
        client.run(input={"action": "load_example"})


def test_run_http_auth_error():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(401, text="Unauthorized")

    transport = httpx.MockTransport(handler)
    client = PepkioClient(api_key="bad-key")
    client._client = httpx.Client(transport=transport, base_url=DEFAULT_API_BASE_URL)

    with pytest.raises(PepkioAuthError, match="Authentication failed"):
        client.run(input={"action": "load_example"})


def test_run_http_500_error():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(500, json={"error": "Internal Server Error"})

    transport = httpx.MockTransport(handler)
    client = PepkioClient(api_key="test-key")
    client._client = httpx.Client(transport=transport, base_url=DEFAULT_API_BASE_URL)

    with pytest.raises(PepkioAPIError, match="Tool execution HTTP error"):
        client.run(input={"action": "load_example"})


def test_run_body_error():
    mock_response = {
        "run_id": "err-run",
        "status": "completed",
        "result": {"error": "document is required"},
        "error": None,
    }

    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=mock_response)

    transport = httpx.MockTransport(handler)
    client = PepkioClient(api_key="test-key")
    client._client = httpx.Client(transport=transport, base_url=DEFAULT_API_BASE_URL)

    with pytest.raises(PepkioAPIError, match="document is required"):
        client.run(input={"action": "scaffold"})


def test_get_run_success():
    mock_run = {
        "run_id": "run-456",
        "status": "completed",
        "result": {"valid": True},
        "error": None,
    }

    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/api/tools/v1/runs/run-456"
        assert request.headers["authorization"] == "Bearer test-key"
        return httpx.Response(200, json=mock_run)

    transport = httpx.MockTransport(handler)
    client = PepkioClient(api_key="test-key")
    client._client = httpx.Client(transport=transport, base_url=DEFAULT_API_BASE_URL)

    res = client.get_run("run-456")
    assert res.run_id == "run-456"
    assert res.status == "completed"
    assert res.result == {"valid": True}
