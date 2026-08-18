"""Pytest configuration and environment loading."""

from pathlib import Path

from dotenv import load_dotenv

# Load root .env file if available for integration test execution
env_path = Path(__file__).resolve().parents[3] / ".env"
if env_path.exists():
    load_dotenv(env_path)
