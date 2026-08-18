"""Python client for Pepkio figure-panel-mockup-grid REST API."""

from .client import FigurePanelMockupGridClient, PepkioClient
from .config import DEFAULT_API_BASE_URL, TOOL_ID
from .exceptions import PepkioAPIError, PepkioAuthError, PepkioError
from .models import (
    AlignConfig,
    FigureDocument,
    FigurePanelInput,
    Panel,
    RunResult,
    ToolManifest,
)

__version__ = "0.1.0"

__all__ = [
    "PepkioClient",
    "FigurePanelMockupGridClient",
    "RunResult",
    "ToolManifest",
    "FigurePanelInput",
    "FigureDocument",
    "Panel",
    "AlignConfig",
    "PepkioError",
    "PepkioAPIError",
    "PepkioAuthError",
    "DEFAULT_API_BASE_URL",
    "TOOL_ID",
]
