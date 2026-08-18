# Pepkio Figure Panel Mockup Grid

Python client and CLI for the Pepkio `figure-panel-mockup-grid` tool REST API.

## Overview
Plan scientific figure layouts with journal presets (Nature, Cell, Science, PNAS), row × column scaffolding, panel alignment, dimension table export (TSV/Markdown), and PDF/PNG mockup specs.

## Installation

```bash
pip install pepkio-figure-panel-mockup-grid
```

## Quickstart

```python
from pepkio_figure_panel_mockup_grid import PepkioClient

client = PepkioClient(api_key="your_pepkio_api_key")

# Scaffold a 2x3 Nature figure layout
result = client.run(
    input={
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
)

print("Run ID:", result.run_id)
print("Panels count:", len(result.result["document"]["panels"]))
```

## CLI Usage

```bash
# Fetch live manifest
pepkio-figure-panel-mockup-grid manifest

# Run built-in example
pepkio-figure-panel-mockup-grid run --example scaffold_2x3

# Run with JSON string input
pepkio-figure-panel-mockup-grid run --input-json '{"action": "load_example"}'
```
