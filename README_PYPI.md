# pepkio-figure-panel-mockup-grid

Programmatic layout grid generator and alignment client for constructing journal-compliant multi-panel scientific figures with automated column width validation.

# What It Does

`pepkio-figure-panel-mockup-grid` provides a Python interface to programmatically design, scaffold, and validate multi-panel figure layouts for scientific publication (*Nature*, *Cell*, *Science*, *PNAS*, and *EMBO Journal*). It automates panel grid calculations across 1-column, 1.5-column, and 2-column specifications, enforces aspect ratio limits, aligns heterogeneous experimental panels, validates canvas dimensions against publisher guidelines, and exports structured asset inventory manifests.

# Features

- **Journal Column Scaffolding**: Automatically calculate panel grid geometry matching *Nature*, *Cell*, *Science*, and *PNAS* column width standards.
- **Programmatic Panel Alignment**: Align panels along top, left, bottom, or right edges and distribute horizontal/vertical spacing evenly.
- **Aspect Ratio Control**: Enforce fixed aspect ratios (`1:1`, `4:3`, `3:2`, `1:2`, or `free`) to prevent distortion of micrographs and blot crops.
- **Experimental Metadata & Scale Bars**: Tag panels (`blot`, `graph`, `micrograph`, `scatter`, `blank`), attach imaging notes, and manage physical scale bar properties.
- **Layout Validation Engine**: Check composite layouts against maximum page height, margin limits, and panel overlap constraints.
- **Inventory Table Export**: Export figure panel asset inventories and coordinate specifications in Tab-Separated Values (TSV) or Markdown format.
- **CLI & Python API**: Execute layout scaffolding and validation programmatically or via command-line tools.

# Installation

```bash
pip install pepkio-figure-panel-mockup-grid
```

# Quick Example

```python
from pepkio_figure_panel_mockup_grid import PepkioClient

# Initialize the Pepkio API client
with PepkioClient(api_key="YOUR_API_KEY") as client:
    # 1. Scaffold a 2x3 grid layout for a Nature 2-column figure (170 mm)
    scaffold_input = {
        "action": "scaffold",
        "rows": 2,
        "cols": 3,
        "document": {
            "journal": "nature",
            "columnWidth": "2-col",
            "marginMm": 3.0,
            "gapMm": 2.5,
            "labelStyle": "uppercase",
        },
    }
    scaffold_res = client.run(scaffold_input)
    document = scaffold_res.result["document"]

    # 2. Add panel type tags, imaging notes, and scale bar settings
    document["panels"][0]["typeTag"] = "micrograph"
    document["panels"][0]["facilityNote"] = "Confocal GFP staining (63x Oil)"
    document["panels"][0]["showScaleBar"] = True
    document["panels"][0]["scaleBarLength"] = "10 µm"
    document["panels"][0]["aspectLock"] = "1:1"

    # 3. Validate layout geometry against Nature publisher limits
    val_res = client.run({"action": "validate", "document": document})
    print("Layout Valid:", val_res.result.get("valid", True))

    # 4. Export the figure panel inventory as a Markdown table
    table_res = client.run({"action": "export_table", "format": "markdown", "document": document})
    print("\nFigure Inventory Table:\n")
    print(table_res.result["table_text"])
```

# Typical Use Cases

- **Manuscript Composite Figure Assembly**: Plan 2-column composite figures combining Western blot crops, qPCR graphs, and confocal microscopy grids for manuscript submission.
- **Microscopy & Immunofluorescence Layout Planning**: Scaffold multi-channel immunofluorescence grids (Control vs. Treatment) with enforced 1:1 square aspect ratios and $10\ \mu\text{m}$ scale bars.
- **Western Blot Gel Crop Alignment**: Structure multi-antibody blotting experiments with aligned gel band panels, ladder lane positions (kDa), and corresponding densitometry graphs.
- **Flow Cytometry & Gating Panels**: Arrange multi-sample gating scatter plots, UMAP dimensionality reduction projections, and population charts into uniform grids.
- **Asset Inventory & Lab Notebook Documentation**: Export detailed TSV or Markdown metadata tables listing panel IDs, image asset paths, acquisition notes, and scale bar lengths.

# Scientific Background

Major scientific journals strictly enforce physical page column widths—such as *Nature* (89 mm single-column, 170 mm double-column), *Cell* (85 mm / 174 mm), and *Science* (55 mm / 175 mm)—to guarantee readable typography and figure legibility in print and PDF formats. Manual layout in general vector graphics editors often leads to improper width scaling, non-standard font sizes, distorted aspect ratios, or misaligned scale bars. Programmatic layout scaffolding computes panel widths ($W_{\text{panel}}$), gap spacing ($G$), and canvas heights based on explicit publisher constraints ($W_{\text{canvas}} = 2M + C \cdot W_{\text{panel}} + (C - 1)G$), ensuring layout compliance and structured metadata management prior to final graphic production.

# Web Application

For researchers who prefer a graphical interface, an interactive web version is available.

Web Application: https://www.pepkio.com/tools/figure-panel-mockup-grid

Web-only features include interactive drag-and-drop grid creation, real-time column width guides, visual canvas rendering, shareable permalinks, and interactive asset manifest worksheets.

# Documentation and Resources

GitHub Repository: https://github.com/pepkio/pepkio-figure-panel-mockup-grid

Web Application: https://www.pepkio.com/tools/figure-panel-mockup-grid

Source code and issue tracking are maintained on [GitHub](https://github.com/pepkio/pepkio-figure-panel-mockup-grid).

# About Pepkio

Pepkio (https://www.pepkio.com/) develops software tools and bioinformatics solutions for life science researchers, including laboratory calculators and analysis services (https://www.pepkio.com/cro). Explore additional online laboratory calculators and workflow tools at https://www.pepkio.com.

# Keywords

* scientific figure panel
* figure layout grid
* journal column width
* figure panel mockup
* publication figure
* multi-panel figure
* figure alignment
* Nature figure layout
* Cell figure layout
* Science figure layout
* PNAS figure layout
* Western blot layout
* microscopy figure grid
* scale bar annotation
* aspect ratio lock
* panel scaffolding
* figure inventory table
* figure metadata
* composite figure builder
* figure grid generator
* bioinformatic figure tool
* manuscript layout validator
* figure panel renumbering
* scientific illustration grid
* manuscript figure prep
* scientific figure grid generator
* journal compliant figure layout
* multi panel Western blot grid
* fluorescence microscopy panel layout
* publication column width validator
* automated figure panel alignment
* figure panel inventory export
* single column figure layout
* double column figure layout
* multi panel scientific illustration
* scientific figure layout planning
* Python client for scientific figures
* scientific figure panel scaffolding
* manuscript composite figure layout
