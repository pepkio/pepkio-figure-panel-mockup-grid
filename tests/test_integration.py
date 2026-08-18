"""Integration tests against live Pepkio API endpoints.

Requires PEPKIO_API_KEY environment variable (or LOCAL_PEPKIO_API_KEY for local test server).
Skipped automatically if no API key is set.
"""

import os

import pytest

from pepkio_figure_panel_mockup_grid import DEFAULT_API_BASE_URL, TOOL_ID, PepkioClient


@pytest.fixture
def api_base_url():
    return os.getenv("PEPKIO_API_BASE_URL", DEFAULT_API_BASE_URL)


@pytest.fixture
def api_key(api_base_url):
    if "localtest.me" in api_base_url:
        key = os.getenv("LOCAL_PEPKIO_API_KEY") or os.getenv("PEPKIO_API_KEY")
    else:
        key = os.getenv("PEPKIO_API_KEY")
    if not key:
        pytest.skip("PEPKIO_API_KEY (or LOCAL_PEPKIO_API_KEY) is not set")
    return key


def test_live_manifest(api_base_url):
    client = PepkioClient(base_url=api_base_url)
    manifest = client.get_manifest()

    assert manifest.get("tool_id") == TOOL_ID
    assert "input" in manifest
    assert "output" in manifest
    assert isinstance(manifest.get("examples"), list)


def test_live_run_scaffold(api_base_url, api_key):
    client = PepkioClient(api_key=api_key, base_url=api_base_url)
    input_payload = {
        "action": "scaffold",
        "rows": 2,
        "cols": 3,
        "document": {
            "journal": "nature",
            "columnWidth": "2-col",
            "canvasHeightMm": 160,
            "gapMm": 2,
            "labelStyle": "uppercase",
            "showGrid": True,
            "panels": [],
        },
    }

    result = client.run(input=input_payload)

    assert result.run_id is not None
    assert result.status == "completed"
    assert result.error is None
    assert result.result is not None
    assert "document" in result.result
    assert len(result.result["document"].get("panels", [])) == 6


def test_live_run_export_table_tsv(api_base_url, api_key):
    client = PepkioClient(api_key=api_key, base_url=api_base_url)
    input_payload = {
        "action": "export_table",
        "format": "tsv",
        "document": {
            "journal": "nature",
            "columnWidth": "2-col",
            "canvasHeightMm": 120,
            "gapMm": 2,
            "labelStyle": "uppercase",
            "showGrid": True,
            "panels": [
                {
                    "id": "p1",
                    "x": 0,
                    "y": 0,
                    "width": 56,
                    "height": 45,
                    "typeTag": "micrograph",
                    "facilityNote": "DAPI / 40x",
                    "aspectLock": "4:3",
                }
            ],
        },
    }

    result = client.run(input=input_payload)

    assert result.run_id is not None
    assert result.status == "completed"
    assert result.result is not None
    assert result.result.get("mime_type") == "text/tab-separated-values"


def test_live_get_run(api_base_url, api_key):
    client = PepkioClient(api_key=api_key, base_url=api_base_url)
    input_payload = {"action": "load_example"}

    run_res = client.run(input=input_payload)
    assert run_res.run_id is not None

    fetched = client.get_run(run_res.run_id)
    assert fetched.run_id == run_res.run_id
    assert fetched.status == "completed"
