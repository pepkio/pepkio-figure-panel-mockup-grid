"""Pydantic models for figure-panel-mockup-grid requests, responses, and manifests."""

from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel, Field

ActionType = Literal[
    "scaffold",
    "export_table",
    "align",
    "validate",
    "load_example",
    "renumber_labels",
]
JournalType = Literal["nature", "cell", "science", "pnas", "custom"]
ColumnWidthType = Literal["1-col", "1.5-col", "2-col"]
LabelStyleType = Literal[
    "uppercase",
    "lowercase",
    "bold_uppercase",
    "bold_lowercase",
    "parentheses",
    "period",
    "numeric",
]
PanelTypeTag = Literal["blot", "graph", "micrograph", "scatter", "blank"]
AspectLockType = Literal["free", "1:1", "4:3", "3:2", "1:2"]
LabelPositionType = Literal["inside-top-left", "inside-top-right", "outside-top-left"]
AlignActionType = Literal[
    "align_top",
    "align_left",
    "align_bottom",
    "align_right",
    "distribute_h",
    "distribute_v",
]
FormatType = Literal["tsv", "markdown"]


class Panel(BaseModel):
    """Scientific figure panel model."""

    id: Optional[str] = None
    x: Optional[float] = None
    y: Optional[float] = None
    width: Optional[float] = None
    height: Optional[float] = None
    typeTag: Optional[PanelTypeTag] = None
    facilityNote: Optional[str] = None
    aspectLock: Optional[AspectLockType] = None
    labelOverride: Optional[str] = None
    labelPosition: Optional[LabelPositionType] = None
    locked: Optional[bool] = None
    showScaleBar: Optional[bool] = None
    scaleBarLength: Optional[str] = None

    model_config = {"extra": "allow"}


class FigureDocument(BaseModel):
    """Figure document canvas and panel collection."""

    journal: Optional[JournalType] = "nature"
    columnWidth: Optional[ColumnWidthType] = "2-col"
    customCanvasWidth: Optional[float] = None
    customCanvasHeight: Optional[float] = None
    canvasHeightMm: Optional[float] = None
    marginMm: Optional[float] = None
    gapMm: Optional[float] = None
    labelStyle: Optional[LabelStyleType] = "uppercase"
    showGrid: Optional[bool] = True
    panels: Optional[List[Panel]] = Field(default_factory=list)

    model_config = {"extra": "allow"}


class AlignConfig(BaseModel):
    """Panel alignment action configuration."""

    action: AlignActionType
    panel_ids: List[str]

    model_config = {"extra": "allow"}


class FigurePanelInput(BaseModel):
    """Tool execution input model for figure-panel-mockup-grid."""

    action: ActionType
    document: Optional[FigureDocument] = None
    rows: Optional[int] = None
    cols: Optional[int] = None
    format: Optional[FormatType] = None
    align: Optional[AlignConfig] = None

    model_config = {"extra": "allow"}


class RunOptions(BaseModel):
    """Options for tool execution request."""

    idempotency_key: Optional[str] = None
    label: Optional[str] = None
    share: Optional[str] = None

    model_config = {"extra": "allow"}


class RunResult(BaseModel):
    """Result payload returned by Pepkio tool run or GET run endpoint."""

    run_id: str
    status: str
    result: Optional[Dict[str, Any]] = None
    error: Optional[Any] = None
    duration_ms: Optional[int] = None
    result_url: Optional[str] = None
    permalink: Optional[str] = None
    tool_id: Optional[str] = None
    label: Optional[str] = None
    input: Optional[Dict[str, Any]] = None
    artifacts: Optional[List[Dict[str, Any]]] = None
    created_at: Optional[str] = None

    model_config = {"extra": "allow"}


class ManifestExample(BaseModel):
    """Example payload included in tool manifest."""

    name: str
    input: Dict[str, Any]
    output: Optional[Dict[str, Any]] = None

    model_config = {"extra": "allow"}


class ToolManifest(BaseModel):
    """Tool manifest contract definition."""

    schema_version: str
    tool_id: str
    title: str
    description: str
    tags: List[str]
    category: str
    execution_mode: str
    estimated_runtime_sec: int
    input: Dict[str, Any]
    output: Dict[str, Any]
    agent_notes: Optional[str] = None
    example_prompts: Optional[List[str]] = None
    examples: List[ManifestExample] = Field(default_factory=list)
    limits: Optional[Dict[str, Any]] = None
    input_schema: Optional[Dict[str, Any]] = None

    model_config = {"extra": "allow"}
