"""Exception hierarchy for Pepkio API client."""

from typing import Any, Dict, Optional


class PepkioError(Exception):
    """Base exception for all Pepkio library errors."""

    pass


class PepkioAuthError(PepkioError):
    """Raised when authentication fails or API key is missing."""

    pass


class PepkioAPIError(PepkioError):
    """Raised when the Pepkio API returns an HTTP error or response error status."""

    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        response_body: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.response_body = response_body

    def __str__(self) -> str:
        if self.status_code:
            return f"[{self.status_code}] {self.message}"
        return self.message
