"""Configuration management for Pepkio figure-panel-mockup-grid client."""

import os
from typing import Optional

from dotenv import load_dotenv

load_dotenv()

DEFAULT_API_BASE_URL = "https://tools.pepkio.com"
TOOL_ID = "figure-panel-mockup-grid"


def get_api_base_url(base_url: Optional[str] = None) -> str:
    """Resolve API base URL from argument or environment variable."""
    url = base_url or os.getenv("PEPKIO_API_BASE_URL") or DEFAULT_API_BASE_URL
    return url.rstrip("/")


def get_api_key(api_key: Optional[str] = None, base_url: Optional[str] = None) -> Optional[str]:
    """Resolve API key from argument or environment variable.

    Checks LOCAL_PEPKIO_API_KEY first when connecting to a local test server.
    Otherwise checks PEPKIO_API_KEY.
    """
    if api_key:
        return api_key

    resolved_base = get_api_base_url(base_url)
    if "localtest.me" in resolved_base:
        local_key = os.getenv("LOCAL_PEPKIO_API_KEY")
        if local_key:
            return local_key

    return os.getenv("PEPKIO_API_KEY")
