# Figure Panel Mockup Grid

Scaffold journal-compliant scientific figure panel grids, align multi-panel assets, validate canvas column widths, and export panel inventory specifications for manuscript publication in Python and via web interface.

# Overview

Preparing multi-panel figures for peer-reviewed scientific journals (such as *Nature*, *Cell*, *Science*, *PNAS*, and *EMBO Journal*) requires careful alignment, consistent typography, and precise spatial planning. Researchers routinely combine heterogeneous experimental data types—including Western blot chemiluminescence membranes, confocal fluorescence micrographs, quantitative PCR bar charts, flow cytometry scatter plots, structural renderings, and pathway schematics—into single composite figures.

Structuring these multi-panel figures manually in general-purpose design software often introduces geometric inconsistencies, panel overlap, non-standard font sizes, misaligned scale bars, and incorrect canvas dimensions. Submitting figures with improper column widths (such as a 125 mm layout for a journal that strictly enforces 89 mm single-column or 170 mm double-column limits) leads to formatting rejections, delayed manuscript processing, and manual resizing that distorts text labels and aspect ratios.

The **Pepkio Figure Panel Mockup Grid** solves these challenges by providing automated spatial scaffolding, journal column width validation, programmatic panel alignment, tag-based panel metadata management, and asset inventory export. It enables bioinformaticians, molecular biologists, laboratory technicians, and scientific illustrators to construct structured figure mockups that adhere to publisher submission guidelines.

The hosted web tool is available at the [Pepkio Figure Panel Mockup Grid](https://www.pepkio.com/tools/figure-panel-mockup-grid) web application for interactive grid creation and visual layout design. Programmatic integration is supported via a Python client package and command-line interface (CLI).

Common search terms and alternative names for this tool include scientific figure mockup grid, journal panel scaffold generator, publication figure layout planner, multi-panel figure alignment tool, Western blot microscopy figure grid, manuscript figure column width validator, biological figure panel builder, and figure panel inventory exporter.

# Features

- **Journal Column Scaffolding**: Automatically generates $N \times M$ grid scaffolds aligned to standard publication column widths for major scientific publishers (*Nature*, *Cell*, *Science*, *PNAS*, and custom specifications).
- **Programmatic Panel Alignment**: Aligns selected panels along edges (`align_top`, `align_left`, `align_bottom`, `align_right`) and distributes panel spacing evenly across horizontal (`distribute_h`) or vertical (`distribute_v`) axes.
- **Aspect Ratio Locking**: Enforces fixed panel dimensions (`1:1` for microscopy squares, `4:3` for standard microphotographs, `3:2`, `1:2`, or `free`) to prevent aspect ratio distortion during image placement.
- **Experimental Tag Taxonomy**: Annotates individual panels with domain-specific data tags (`blot`, `graph`, `micrograph`, `scatter`, `blank`) alongside facility notes, imaging parameters, and target figure titles.
- **Scale Bar Property Tracking**: Integrates scale bar presence flags and physical unit specifications (e.g., $10\ \mu\text{m}$, $100\ \text{nm}$) directly into panel metadata structures.
- **Label Standardization & Renumbering**: Automatically reformats panel labels across standardized typographic styles (`uppercase`, `lowercase`, `bold_uppercase`, `bold_lowercase`, `parentheses`, `period`, `numeric`) with automatic label re-indexing.
- **Layout Validation Engine**: Verifies layout compliance against target journal margin boundaries, maximum canvas heights, panel overlap constraints, and consistent gap spacing.
- **Table Inventory Export**: Exports structured figure panel inventories and coordinate specifications in Tab-Separated Values (TSV) or Markdown format for laboratory notebooks and submission manifests.
- **CLI & Python API**: Provides an asynchronous and synchronous Python API alongside a Click-based CLI for automated script integration and workflow execution.

# Common Use Cases

- **Manuscript Composite Figure Assembly**: Plan 2-column composite figures combining Western blot crop panels, qPCR bar plots, and fluorescence microscopy grids for *Nature* or *Cell* submissions.
- **Microscopy & Immunofluorescence Layout Planning**: Scaffold multi-condition immunofluorescence panel grids (e.g., Control vs. Knockdown across 3 fluorescence channels) with locked 1:1 square aspect ratios and $10\ \mu\text{m}$ scale bar annotations.
- **Western Blot Gel Crop Alignment**: Structure multi-antibody blotting experiments with aligned gel band panels, molecular weight marker lanes (kDa), and corresponding quantitative signal densitometry graphs.
- **Flow Cytometry & Single-Cell Gating Panels**: Arrange multi-sample gating scatter plots, UMAP/t-SNE dimensionality reduction projections, and population percentage bar charts into uniform grid structures.
- **Scientific Poster & Thesis Figure Scaffolding**: Design structured multi-panel layouts for academic conference posters, doctoral dissertations, and grant proposals.
- **Figure Asset Inventory Management**: Export detailed TSV metadata tables listing panel identifiers, raw image asset paths, imaging facility notes, and scale bar lengths to streamline collaborative manuscript drafting.

# Why This Tool Exists

Conventional vector graphics editors (such as Adobe Illustrator, Inkscape, or Microsoft PowerPoint) lack built-in domain awareness for scientific publication standards. Illustrators must manually calculate pixel-to-millimeter conversions, measure canvas column boundaries, compute uniform panel gaps, and adjust individual panel positions whenever a panel is added or removed.

Furthermore, general-purpose graphics tools do not store structured metadata for individual panels. Information such as exposure times, antibody catalog numbers, scale bar lengths, or raw image file locations must be managed separately in laboratory notebooks or spreadsheets, creating friction during revision cycles or manuscript resubmissions.

The **Pepkio Figure Panel Mockup Grid** addresses these limitations by introducing a structured model for scientific figure geometry. By storing canvas dimensions in physical units (millimeters), enforcing journal column width constraints, providing deterministic grid alignment algorithms, and supporting metadata tagging, the tool bridges the gap between laboratory data collection and journal publication requirements. Researchers can access these layout algorithms online via the [figure panel mockup web calculator](https://www.pepkio.com/tools/figure-panel-mockup-grid) or execute them locally using the Python client package.

# Installation

Install the Python client package from PyPI using `pip`:

```bash
pip install pepkio-figure-panel-mockup-grid
```

Or using `uv`:

```bash
uv add pepkio-figure-panel-mockup-grid
```

Package distribution details and version history are indexed on [PyPI](https://pypi.org/project/pepkio-figure-panel-mockup-grid/).

# Quick Start

### Python API Usage

Set your Pepkio API key as an environment variable:

```bash
export PEPKIO_API_KEY="your_pepkio_api_key"
```

Execute figure scaffolding, alignment, validation, and table export operations in Python:

```python
from pepkio_figure_panel_mockup_grid import PepkioClient, FigureDocument, Panel

# Initialize the client context
with PepkioClient() as client:
    # 1. Scaffold a 2x3 grid layout for a Nature 2-column figure (170 mm width)
    scaffold_input = {
        "action": "scaffold",
        "rows": 2,
        "cols": 3,
        "document": {
            "journal": "nature",
            "columnWidth": "2-col",
            "marginMm": 3.0,
            "gapMm": 2.5,
            "labelStyle": "uppercase"
        }
    }
    scaffold_result = client.run(scaffold_input)
    document = scaffold_result.result["document"]
    print("Scaffolded Panel Count:", len(document["panels"]))
    print("Permalink:", scaffold_result.permalink)

    # 2. Add panel type tags, facility notes, and scale bar flags to panel 'A'
    document["panels"][0]["typeTag"] = "micrograph"
    document["panels"][0]["facilityNote"] = "63x Oil immersion, Channel 488nm"
    document["panels"][0]["showScaleBar"] = True
    document["panels"][0]["scaleBarLength"] = "10 µm"
    document["panels"][0]["aspectLock"] = "1:1"

    # 3. Validate the customized document against Nature journal limits
    val_result = client.run({
        "action": "validate",
        "document": document
    })
    print("Layout Valid:", val_result.result.get("valid", True))

    # 4. Export the figure panel inventory as a Markdown table
    table_result = client.run({
        "action": "export_table",
        "format": "markdown",
        "document": document
    })
    print("\nFigure Panel Inventory Table:\n")
    print(table_result.result["table_text"])
```

### Command Line Interface (CLI)

The package includes a command-line interface executable `pepkio-figure-panel-mockup-grid`:

```bash
# View available manifest information and schemas
pepkio-figure-panel-mockup-grid manifest

# Run a pre-configured example payload from the manifest
pepkio-figure-panel-mockup-grid run --example scaffold_2x3

# Execute a custom JSON input payload
pepkio-figure-panel-mockup-grid run --input-json '{"action": "scaffold", "rows": 2, "cols": 3, "document": {"journal": "cell", "columnWidth": "2-col"}}'

# Fetch details of a previously executed run by ID
pepkio-figure-panel-mockup-grid get-run run_scaffold_12345678
```

Repository source code and developer documentation are maintained on [GitHub](https://github.com/pepkio/pepkio-figure-panel-mockup-grid).

# Example Output

API requests return structured JSON responses containing execution status, processed document models, validation results, formatted inventory tables, and reproducible web permalinks.

### Representative Result Object (`action: scaffold`)

```json
{
  "run_id": "run_scaffold_9876543210",
  "status": "completed",
  "result": {
    "ready": true,
    "document": {
      "journal": "nature",
      "columnWidth": "2-col",
      "customCanvasWidth": null,
      "customCanvasHeight": 225.0,
      "canvasHeightMm": 225.0,
      "marginMm": 3.0,
      "gapMm": 2.5,
      "labelStyle": "uppercase",
      "showGrid": true,
      "panels": [
        {
          "id": "A",
          "x": 3.0,
          "y": 3.0,
          "width": 53.0,
          "height": 53.0,
          "typeTag": "micrograph",
          "facilityNote": "Confocal GFP-Staining 63x",
          "aspectLock": "1:1",
          "labelOverride": null,
          "labelPosition": "inside-top-left",
          "locked": false,
          "showScaleBar": true,
          "scaleBarLength": "10 µm"
        },
        {
          "id": "B",
          "x": 58.5,
          "y": 3.0,
          "width": 53.0,
          "height": 53.0,
          "typeTag": "blot",
          "facilityNote": "Anti-GAPDH Western Blot",
          "aspectLock": "free",
          "labelOverride": null,
          "labelPosition": "inside-top-left",
          "locked": false,
          "showScaleBar": false,
          "scaleBarLength": null
        },
        {
          "id": "C",
          "x": 114.0,
          "y": 3.0,
          "width": 53.0,
          "height": 53.0,
          "typeTag": "graph",
          "facilityNote": "Densitometry qPCR Quantification",
          "aspectLock": "free",
          "labelOverride": null,
          "labelPosition": "inside-top-left",
          "locked": false,
          "showScaleBar": false,
          "scaleBarLength": null
        }
      ]
    },
    "interpretation": "Scaffolded 2x3 grid for Nature 2-column figure layout (170mm width). Total panels: 6.",
    "methods_text": "Panels calculated with margin 3.0mm, gap 2.5mm, and uniform column spanning."
  },
  "error": null,
  "result_url": "https://tools.pepkio.com/api/tools/v1/runs/run_scaffold_9876543210",
  "permalink": "https://tools.pepkio.com/r/run_scaffold_9876543210"
}
```

### Action Modes Overview

| Action Mode | Core Parameters | Output Data | Biological / Manuscript Workflow Context |
| :--- | :--- | :--- | :--- |
| `scaffold` | `rows`, `cols`, `document` | Complete `FigureDocument` with panel coordinates | Initial grid creation for 1-col, 1.5-col, or 2-col publication figures |
| `align` | `align.action`, `align.panel_ids` | Updated panel coordinates within `FigureDocument` | Precise edge alignment (`align_top`, `align_left`) or distribution across axes |
| `validate` | `document` | Boolean `valid`, rule violation list | Pre-submission compliance check against journal canvas height and margin limits |
| `renumber_labels` | `document`, `labelStyle` | Updated panel label identifiers (`id`) | Re-ordering panel labels (A–F, a–f, 1–6) after inserting or deleting panels |
| `export_table` | `document`, `format` (`tsv`/`markdown`) | Formatted table string | Generating supplementary figure asset manifests and lab notebook documentation |
| `load_example` | `example_name` | Pre-configured `FigureDocument` scaffold | Quick loading of standard Western blot + microscopy templates |

# Scientific Background

### Publication Column Width Specifications

Major academic publishers establish strict physical width categories for manuscripts. Figures must be rendered to match these physical width boundaries to ensure legible typography and consistent page composition during print and PDF layout.

| Publisher / Journal | Single Column (1-col) | Intermediate Column (1.5-col) | Double / Full Column (2-col) | Maximum Page Height |
| :--- | :--- | :--- | :--- | :--- |
| **Nature Portfolio** | $89\ \text{mm}$ | $120\text{--}136\ \text{mm}$ | $170\text{--}183\ \text{mm}$ | $225\text{--}235\ \text{mm}$ |
| **Cell Press** | $85\ \text{mm}$ | $114\ \text{mm}$ | $174\ \text{mm}$ | $225\ \text{mm}$ |
| **Science (AAAS)** | $55\ \text{mm}$ ($5.5\ \text{cm}$) | $120\ \text{mm}$ ($12.0\ \text{cm}$) | $175\ \text{mm}$ ($17.5\ \text{cm}$) | $230\ \text{mm}$ |
| **PNAS** | $86\ \text{mm}$ ($8.6\ \text{cm}$) | N/A | $178\ \text{mm}$ ($17.8\ \text{cm}$) | $225\ \text{mm}$ |
| **EMBO Press** | $85\ \text{mm}$ | $120\ \text{mm}$ | $175\ \text{mm}$ | $230\ \text{mm}$ |

### Physical Layout Calculations

The spatial placement of panels within a grid layout is governed by the total available canvas width $W_{\text{canvas}}$, margin size $M$, panel gap $G$, number of columns $C$, and number of rows $R$.

The calculated individual panel width $W_{\text{panel}}$ for a uniform grid is derived as:

$$W_{\text{panel}} = \frac{W_{\text{canvas}} - 2M - (C - 1)G}{C}$$

For a panel positioned at row index $i \in \{0, 1, \dots, R-1\}$ and column index $j \in \{0, 1, \dots, C-1\}$, the top-left coordinate $(x_{ij}, y_{ij})$ is defined by:

$$x_{ij} = M + j \cdot (W_{\text{panel}} + G)$$

$$y_{ij} = M + i \cdot (H_{\text{panel}} + G)$$

Where $H_{\text{panel}}$ is determined either by a designated aspect ratio $AR = \frac{W_{\text{panel}}}{H_{\text{panel}}}$ or by explicit row height settings:

$$H_{\text{panel}} = \frac{W_{\text{panel}}}{AR}$$

### Digital Image Resolution & Physical Scaling

Scientific figures must satisfy publisher digital resolution requirements upon export:

$$\text{Pixel Dimension (px)} = \frac{\text{Physical Size (mm)}}{25.4\ \text{mm/inch}} \times \text{DPI}$$

- **Monochrome Line Art & Vector Graphs**: $1000\text{--}1200\ \text{DPI}$
- **Combination Figures (Halftone + Line Art)**: $500\text{--}600\ \text{DPI}$
- **Color Photographic Images & Micrographs**: $300\text{--}450\ \text{DPI}$

For example, a $170\ \text{mm}$ 2-column figure rendered at $300\ \text{DPI}$ requires a minimum raster image width of:

$$\text{Width}_{\text{px}} = \frac{170}{25.4} \times 300 \approx 2007.87 \approx 2008\ \text{pixels}$$

### Scale Bar Magnification Math

Scale bars on fluorescence micrographs or electron microscopy images indicate true physical dimensions. The scale bar pixel length $L_{\text{px}}$ is computed relative to the full field of view (FOV) physical width $W_{\text{FOV}}$ and image pixel width $W_{\text{img}}$:

$$L_{\text{px}} = \frac{L_{\text{scale}}(\mu\text{m}) \times W_{\text{img}}(\text{px})}{W_{\text{FOV}}(\mu\text{m})}$$

Maintaining scale bar accuracy across multi-panel grids prevents scientific misrepresentation when panels undergo proportional resizing during scaffold assembly.

# Frequently Asked Questions

### What is a scientific figure panel mockup grid?
A scientific figure panel mockup grid is a spatial layout framework used by researchers to plan, dimension, and organize multi-panel figures before final publication assembly. It establishes canvas boundaries, panel coordinates, gaps, margins, and label positions in accordance with journal submission standards.

### What are the standard column widths for *Nature*, *Cell*, and *Science* figures?
Standard single-column (1-col) widths range from $55\ \text{mm}$ (*Science*) to $85\ \text{mm}$ (*Cell*) and $89\ \text{mm}$ (*Nature*). Double-column (2-col) widths range from $170\ \text{mm}$ (*Nature*) to $174\ \text{mm}$ (*Cell*), $175\ \text{mm}$ (*Science*), and $178\ \text{mm}$ (*PNAS*).

### How do I calculate panel dimensions for a 2-column *Nature* figure?
For a $170\ \text{mm}$ canvas width with $3\ \text{mm}$ left/right margins and a $3\ \text{mm}$ gap between 2 columns, each panel width is calculated as $(170 - 2(3) - 3) / 2 = 79\ \text{mm}$.

### Why is aspect ratio locking important for microscopy panels?
Locking aspect ratios (such as `1:1` for square confocal images or `4:3` for standard CCD sensors) prevents image stretching or compression during layout adjustments, preserving accurate cell morphology and spatial proportions.

### How does automatic panel label renumbering work?
The renumbering engine parses panel collections and updates label tags according to a specified typographic style (such as `uppercase` A, B, C; `lowercase` a, b, c; or `bold_uppercase` **A**, **B**, **C**), maintaining logical ordering when panels are added, removed, or reordered.

### Can I export figure layout metadata to a spreadsheet or table?
Yes. The tool exports panel metadata—including panel IDs, X/Y coordinates, dimensions, experimental tags (`blot`, `micrograph`, `graph`, `scatter`), scale bar specifications, and facility notes—as TSV or Markdown tables.

### How do I ensure my figure labels meet journal font size requirements?
Publishers typically require figure panel labels to be set in sans-serif fonts (such as Arial or Helvetica) between 6 pt and 8 pt at final publication size. Planning canvas dimensions at 100% physical scale prevents label scaling distortions.

### What experimental data tags are supported?
The tool supports domain-specific tags including `blot` (Western/Northern/Southern gel membranes), `graph` (qPCR/densitometry bar plots and line charts), `micrograph` (confocal/light/electron microscopy images), `scatter` (flow cytometry/single-cell gating plots), and `blank` (schematics and structural diagrams).

### How does the tool handle panel alignment and equal distribution?
The alignment module provides operations to align selected panels along common edges (`align_top`, `align_left`, `align_bottom`, `align_right`) and distribute spacing evenly horizontally (`distribute_h`) or vertically (`distribute_v`).

### What is the difference between 1-column, 1.5-column, and 2-column layouts?
A 1-column layout occupies a single column of a multi-column page format. A 1.5-column layout spans intermediate widths ($114\text{--}136\ \text{mm}$) leaving room for side captions. A 2-column layout spans the full printable page width ($170\text{--}178\ \text{mm}$).

### How does layout validation prevent manuscript formatting rejection?
The validation engine checks layout documents against target journal bounds, flagging panel overlaps, off-canvas positioning, inconsistent panel gaps, and total height violations before manuscript submission.

### How do I specify scale bar lengths in microscopy figure panels?
Scale bar properties can be assigned directly to individual panel metadata models by setting `showScaleBar` to `true` and defining `scaleBarLength` (e.g., `"10 µm"` or `"500 nm"`).

### How do I use the Python client offline or with custom API endpoints?
Initialize `PepkioClient` with a custom `base_url` parameter or set the `PEPKIO_API_BASE_URL` environment variable. The client handles HTTP requests, authentication headers, and response parsing.

### What file formats should be used for final figure vector assembly?
While this tool plans geometric mockups and exports layout specifications, final figure assembly for journal submission should be saved in EPS, PDF, SVG, or high-resolution TIFF format (300–1200 DPI).

### Can I share interactive figure mockups with co-authors?
Yes. Web tool runs and Python API execution results generate permanent URLs (`permalink`) that allow research team members to view and inspect figure layout specifications online.

# Web Application

The hosted web application provides an interactive graphical workspace for designing, scaffolding, and validating scientific figure layouts directly in the browser.

The web version provides an interactive interface, shareable links, protocol generation, printable worksheets, and visualization tools.

Access the interactive web tool at:  
Web Application:  
https://www.pepkio.com/tools/figure-panel-mockup-grid

# Related Resources

Access project repositories, software packages, and documentation via the following links:

GitHub Repository:  
https://github.com/pepkio/pepkio-figure-panel-mockup-grid

PyPI Package:  
https://pypi.org/project/pepkio-figure-panel-mockup-grid/

Web Application:  
https://www.pepkio.com/tools/figure-panel-mockup-grid

# About Pepkio

Pepkio (https://www.pepkio.com/) develops software tools and bioinformatics solutions for life science researchers, including laboratory calculators and analysis services (https://www.pepkio.com/cro).

Pepkio provides technical workflows and data processing capabilities across multiple biological domains, including:
- RNA-seq analysis
- Single-cell RNA-seq analysis
- Spatial transcriptomics analysis
- Functional enrichment analysis
- Custom bioinformatics workflows

Website:  
https://www.pepkio.com/

# Citation

If you use the Pepkio Figure Panel Mockup Grid in your research, manuscript preparation, or bioinformatics pipelines, please cite the software as follows:

```bibtex
@software{pepkio_figure_panel_mockup_grid_2026,
  author       = {{Pepkio Bioanalytics Team}},
  title        = {Pepkio Figure Panel Mockup Grid: Layout Scaffolding and Journal Column Width Validation for Scientific Publications},
  year         = {2026},
  publisher    = {Pepkio},
  url          = {https://www.pepkio.com/tools/figure-panel-mockup-grid},
  note         = {Python package version 0.1.0}
}
```

# License

This project is licensed under the MIT License. See the `LICENSE` file in the software repository for full details.

# Keywords

figure panel mockup grid, scientific figure layout builder, journal panel scaffold generator, publication figure alignment tool, Western blot microscopy figure planner, manuscript figure column width validator, biological figure grid generator, multi-panel figure builder, Nature figure column width calculator, Cell press figure layout tool, Science journal figure dimensions, PNAS figure panel template, immunofluorescence panel grid builder, confocal image aspect ratio lock, flow cytometry gating panel layout, qPCR densitometry bar plot grid, scientific figure panel inventory TSV, panel label renumbering tool, scale bar metadata tracker, microphotograph layout manager, multi-column composite figure scaffold, bioinformatic figure designer, figure panel coordinate solver, manuscript submission figure validator, vector graphics grid planner, scientific image panel spacing tool, biological figure layout software, figure panel manifest exporter, peer-reviewed paper figure generator, high-throughput assay layout grid

scientific figure panel layout generator for Nature, how to plan 2-column composite figures for Cell press, Western blot and immunofluorescence panel grid builder, standard column width dimensions for Science journal figures, automated panel label renumbering and typography formatting, export figure panel asset inventory as TSV table, confocal microscopy scale bar length metadata tracking, prevent aspect ratio distortion in scientific figure panels, layout validation engine for manuscript figure submission, Python REST API client for scientific figure scaffolding, multi-panel grid alignment and spacing distribution, command line interface for figure panel mockup grid, scientific poster and thesis figure panel planner, biological image layout optimization and column width validation
