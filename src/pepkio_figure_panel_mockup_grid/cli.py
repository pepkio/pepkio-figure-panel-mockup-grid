"""Command line interface for pepkio-figure-panel-mockup-grid."""

import json
import sys
from typing import Any, Dict, Optional

import click

from .client import PepkioClient
from .config import DEFAULT_API_BASE_URL
from .exceptions import PepkioError


@click.group()
@click.version_option(package_name="pepkio-figure-panel-mockup-grid")
def main() -> None:
    """Pepkio figure-panel-mockup-grid CLI.

    Interact with the Pepkio REST API for planning scientific figure panel layouts.
    """
    pass


@main.command()
@click.option(
    "--base-url",
    default=None,
    help=f"API base URL (default: {DEFAULT_API_BASE_URL} or PEPKIO_API_BASE_URL env var)",
)
@click.option(
    "--api-key",
    default=None,
    help="Pepkio API key (default: PEPKIO_API_KEY env var)",
)
def manifest(base_url: Optional[str], api_key: Optional[str]) -> None:
    """Fetch and display the tool manifest."""
    try:
        client = PepkioClient(api_key=api_key, base_url=base_url)
        data = client.get_manifest()
        click.echo(json.dumps(data, indent=2))
    except PepkioError as exc:
        click.echo(f"Error: {exc}", err=True)
        sys.exit(1)
    except Exception as exc:
        click.echo(f"Unexpected error: {exc}", err=True)
        sys.exit(1)


@main.command()
@click.option(
    "--example",
    "example_name",
    default=None,
    help="Name of example payload from manifest (e.g., scaffold_2x3, export_table_tsv)",
)
@click.option(
    "--input-json",
    default=None,
    help="Raw JSON input string",
)
@click.option(
    "--input-file",
    type=click.Path(exists=True, dir_okay=False, readable=True),
    default=None,
    help="Path to JSON file containing tool input",
)
@click.option(
    "--base-url",
    default=None,
    help=f"API base URL (default: {DEFAULT_API_BASE_URL} or PEPKIO_API_BASE_URL env var)",
)
@click.option(
    "--api-key",
    default=None,
    help="Pepkio API key (default: PEPKIO_API_KEY env var)",
)
@click.option(
    "--idempotency-key",
    default=None,
    help="Optional idempotency key for run request",
)
@click.option(
    "--label",
    default=None,
    help="Optional run label",
)
def run(
    example_name: Optional[str],
    input_json: Optional[str],
    input_file: Optional[str],
    base_url: Optional[str],
    api_key: Optional[str],
    idempotency_key: Optional[str],
    label: Optional[str],
) -> None:
    """Run the figure-panel-mockup-grid tool over REST API."""
    client = PepkioClient(api_key=api_key, base_url=base_url)
    input_data: Optional[Dict[str, Any]] = None

    if example_name:
        try:
            manifest_data = client.get_manifest()
            examples = manifest_data.get("examples", [])
            matched = next((ex for ex in examples if ex.get("name") == example_name), None)
            if not matched:
                avail = ", ".join(ex.get("name", "") for ex in examples if "name" in ex)
                click.echo(
                    f"Error: Example '{example_name}' not found. Available examples: {avail}",
                    err=True,
                )
                sys.exit(1)
            input_data = matched.get("input", {})
        except PepkioError as exc:
            click.echo(f"Error fetching manifest for example: {exc}", err=True)
            sys.exit(1)

    elif input_json:
        try:
            input_data = json.loads(input_json)
        except json.JSONDecodeError as exc:
            click.echo(f"Error: Invalid JSON string for --input-json: {exc}", err=True)
            sys.exit(1)

    elif input_file:
        try:
            with open(input_file, "r", encoding="utf-8") as f:
                input_data = json.load(f)
        except Exception as exc:
            click.echo(f"Error reading file '{input_file}': {exc}", err=True)
            sys.exit(1)

    else:
        click.echo(
            "Error: Must specify one of --example, --input-json, or --input-file",
            err=True,
        )
        sys.exit(1)

    try:
        result = client.run(
            input=input_data,
            idempotency_key=idempotency_key,
            label=label,
        )
        click.echo(json.dumps(result.model_dump(exclude_none=True), indent=2))
    except PepkioError as exc:
        click.echo(f"Error: {exc}", err=True)
        sys.exit(1)
    except Exception as exc:
        click.echo(f"Unexpected error: {exc}", err=True)
        sys.exit(1)


@main.command("get-run")
@click.argument("run_id")
@click.option(
    "--base-url",
    default=None,
    help=f"API base URL (default: {DEFAULT_API_BASE_URL} or PEPKIO_API_BASE_URL env var)",
)
@click.option(
    "--api-key",
    default=None,
    help="Pepkio API key (default: PEPKIO_API_KEY env var)",
)
def get_run(run_id: str, base_url: Optional[str], api_key: Optional[str]) -> None:
    """Fetch status and result for a specific run ID."""
    try:
        client = PepkioClient(api_key=api_key, base_url=base_url)
        result = client.get_run(run_id)
        click.echo(json.dumps(result.model_dump(exclude_none=True), indent=2))
    except PepkioError as exc:
        click.echo(f"Error: {exc}", err=True)
        sys.exit(1)
    except Exception as exc:
        click.echo(f"Unexpected error: {exc}", err=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
