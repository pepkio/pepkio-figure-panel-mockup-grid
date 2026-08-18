# Pepkio Figure Panel Mockup Grid

Python client for the Pepkio `figure-panel-mockup-grid` REST API.

## Overview
Plan scientific figure layouts with journal presets (Nature, Cell, Science, PNAS), panel alignment, and dimension table export.

## Installation

```bash
pip install pepkio-figure-panel-mockup-grid
```

## Usage

```python
from pepkio_figure_panel_mockup_grid import PepkioClient

client = PepkioClient(api_key="your_pepkio_api_key")
manifest = client.get_manifest()
result = client.run(input={"action": "load_example"})
print(result.status)
```
