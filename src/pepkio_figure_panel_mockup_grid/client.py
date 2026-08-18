"""Pepkio REST API client for figure-panel-mockup-grid tool."""

import time
from typing import Any, Dict, Optional, Union

import httpx
from pydantic import BaseModel

from .config import TOOL_ID, get_api_base_url, get_api_key
from .exceptions import PepkioAPIError, PepkioAuthError
from .models import FigurePanelInput, RunResult, ToolManifest


class PepkioClient:
    """Client for Pepkio figure-panel-mockup-grid REST API.

    Usage:
        client = PepkioClient(api_key="ahx_live_...")
        manifest = client.get_manifest()
        result = client.run(input={"action": "scaffold", "rows": 2, "cols": 3, ...})
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: float = 30.0,
        verify: Optional[bool] = None,
    ) -> None:
        self.base_url = get_api_base_url(base_url)
        self.api_key = get_api_key(api_key, base_url=self.base_url)
        self.timeout = timeout
        if verify is None:
            self.verify = False if "localtest.me" in self.base_url else True
        else:
            self.verify = verify
        self._client: Optional[httpx.Client] = None

    def _get_httpx_client(self) -> httpx.Client:
        if self._client is None or self._client.is_closed:
            self._client = httpx.Client(
                base_url=self.base_url,
                timeout=self.timeout,
                verify=self.verify,
            )
        return self._client

    def __enter__(self) -> "PepkioClient":
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self.close()

    def close(self) -> None:
        """Close the underlying HTTP client session."""
        if self._client is not None and not self._client.is_closed:
            self._client.close()

    def _headers(self, require_auth: bool = True) -> Dict[str, str]:
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        elif require_auth:
            raise PepkioAuthError(
                "API key is required. Set PEPKIO_API_KEY environment variable "
                "or pass api_key to PepkioClient."
            )
        return headers

    def get_manifest(self) -> Dict[str, Any]:
        """Fetch tool manifest containing input schema, examples, and metadata.

        Returns:
            Dict[str, Any]: Live manifest JSON dict.
        """
        client = self._get_httpx_client()
        url = f"/api/tools/v1/tools/{TOOL_ID}/manifest"
        headers = self._headers(require_auth=False)

        try:
            response = client.get(url, headers=headers)
        except httpx.HTTPError as exc:
            raise PepkioAPIError(f"HTTP request failed: {exc}") from exc

        if response.status_code in (401, 403):
            raise PepkioAuthError(
                f"Authentication failed ({response.status_code}): {response.text}"
            )
        if response.status_code >= 400:
            is_json = response.headers.get("content-type", "").startswith("application/json")
            resp_body = response.json() if is_json else None
            raise PepkioAPIError(
                f"Failed to fetch manifest ({response.status_code})",
                status_code=response.status_code,
                response_body=resp_body,
            )

        return response.json()

    def get_typed_manifest(self) -> ToolManifest:
        """Fetch tool manifest and parse into a typed ToolManifest Pydantic model."""
        raw_manifest = self.get_manifest()
        return ToolManifest.model_validate(raw_manifest)

    def run(
        self,
        input: Union[Dict[str, Any], FigurePanelInput, BaseModel],
        *,
        idempotency_key: Optional[str] = None,
        label: Optional[str] = None,
        share: Optional[str] = None,
    ) -> RunResult:
        """Execute the figure-panel-mockup-grid tool over REST API.

        Args:
            input: Tool-specific input payload (dict or Pydantic model).
            idempotency_key: Optional idempotency token.
            label: Optional label for run identification.
            share: Optional sharing configuration.

        Returns:
            RunResult: Run response containing run_id, status, and result payload.
        """
        if isinstance(input, BaseModel):
            input_dict = input.model_dump(exclude_unset=True)
        elif isinstance(input, dict):
            input_dict = input
        else:
            raise ValueError("input must be a dict or Pydantic model")

        options: Dict[str, Any] = {}
        if idempotency_key:
            options["idempotency_key"] = idempotency_key
        if label:
            options["label"] = label
        if share:
            options["share"] = share

        payload: Dict[str, Any] = {"input": input_dict}
        if options:
            payload["options"] = options

        client = self._get_httpx_client()
        url = f"/api/tools/v1/tools/{TOOL_ID}/run"
        headers = self._headers(require_auth=True)

        try:
            response = client.post(url, headers=headers, json=payload)
        except httpx.HTTPError as exc:
            raise PepkioAPIError(f"HTTP request failed: {exc}") from exc

        if response.status_code in (401, 403):
            raise PepkioAuthError(
                f"Authentication failed ({response.status_code}): {response.text}"
            )
        if response.status_code >= 400:
            resp_body = None
            try:
                resp_body = response.json()
            except Exception:
                pass
            raise PepkioAPIError(
                f"Tool execution HTTP error ({response.status_code}): {response.text}",
                status_code=response.status_code,
                response_body=resp_body,
            )

        data = response.json()
        run_result = RunResult.model_validate(data)

        # Check for error in response body or result payload
        if run_result.error is not None:
            err_msg = str(run_result.error)
            raise PepkioAPIError(f"Tool run returned error: {err_msg}", response_body=data)
        if isinstance(run_result.result, dict) and run_result.result.get("error"):
            err_msg = str(run_result.result["error"])
            raise PepkioAPIError(f"Tool run execution error: {err_msg}", response_body=data)

        return run_result

    def get_run(self, run_id: str) -> RunResult:
        """Fetch the status and result of a run by ID.

        Args:
            run_id: Unique identifier for the run.

        Returns:
            RunResult: Run details and output result.
        """
        if not run_id:
            raise ValueError("run_id is required")

        client = self._get_httpx_client()
        url = f"/api/tools/v1/runs/{run_id}"
        headers = self._headers(require_auth=True)

        try:
            response = client.get(url, headers=headers)
        except httpx.HTTPError as exc:
            raise PepkioAPIError(f"HTTP request failed: {exc}") from exc

        if response.status_code in (401, 403):
            raise PepkioAuthError(
                f"Authentication failed ({response.status_code}): {response.text}"
            )
        if response.status_code >= 400:
            resp_body = None
            try:
                resp_body = response.json()
            except Exception:
                pass
            raise PepkioAPIError(
                f"Get run HTTP error ({response.status_code}): {response.text}",
                status_code=response.status_code,
                response_body=resp_body,
            )

        data = response.json()
        return RunResult.model_validate(data)

    def poll_run(
        self,
        run_id: str,
        poll_interval: float = 1.0,
        max_attempts: int = 60,
    ) -> RunResult:
        """Poll get_run until the run status is 'completed' or 'failed'.

        Args:
            run_id: Run ID to poll.
            poll_interval: Seconds to wait between polls.
            max_attempts: Maximum number of polling attempts.

        Returns:
            RunResult: Final completed or failed RunResult object.
        """
        attempts = 0
        while attempts < max_attempts:
            result = self.get_run(run_id)
            if result.status in ("completed", "failed", "errored"):
                return result
            time.sleep(poll_interval)
            attempts += 1

        raise PepkioAPIError(f"Run {run_id} timed out after {max_attempts * poll_interval} seconds")


# Convenient alias
FigurePanelMockupGridClient = PepkioClient
