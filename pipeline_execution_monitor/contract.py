from dataclasses import dataclass, field
from typing import Any


VALID_PIPELINE_STATUSES = {
    "waiting",
    "running",
    "completed",
    "failed",
    "blocked",
    "skipped",
    "unknown",
}

VALID_NODE_STATUSES = {
    "waiting",
    "running",
    "completed",
    "failed",
    "blocked",
    "skipped",
    "unknown",
}

VALID_TIMELINE_EVENTS = {
    "pipeline_started",
    "pipeline_finished",
    "node_started",
    "node_finished",
    "node_failed",
    "node_skipped",
    "node_blocked",
    "status_changed",
    "metric_recorded",
}


@dataclass(frozen=True)
class PipelineExecutionState:
    pipeline_id: str
    status: str
    started_at: str | None = None
    finished_at: str | None = None
    duration_seconds: float | None = None

    def __post_init__(self) -> None:
        if not self.pipeline_id:
            raise ValueError("pipeline_id is required")

        if self.status not in VALID_PIPELINE_STATUSES:
            raise ValueError(f"invalid pipeline status: {self.status}")


@dataclass(frozen=True)
class NodeExecutionState:
    node_id: str
    node_name: str
    status: str
    started_at: str | None = None
    finished_at: str | None = None
    duration_seconds: float | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.node_id:
            raise ValueError("node_id is required")

        if not self.node_name:
            raise ValueError("node_name is required")

        if self.status not in VALID_NODE_STATUSES:
            raise ValueError(f"invalid node status: {self.status}")


@dataclass(frozen=True)
class TimelineEvent:
    timestamp: str
    event: str
    node_id: str | None = None
    message: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.timestamp:
            raise ValueError("timestamp is required")

        if self.event not in VALID_TIMELINE_EVENTS:
            raise ValueError(f"invalid timeline event: {self.event}")


@dataclass(frozen=True)
class MonitorMetrics:
    total_nodes: int
    completed_nodes: int = 0
    running_nodes: int = 0
    failed_nodes: int = 0
    skipped_nodes: int = 0
    blocked_nodes: int = 0
    waiting_nodes: int = 0
    success_rate: float = 0.0
    elapsed_seconds: float | None = None

    def __post_init__(self) -> None:
        if self.total_nodes < 0:
            raise ValueError("total_nodes cannot be negative")

        numeric_fields = {
            "completed_nodes": self.completed_nodes,
            "running_nodes": self.running_nodes,
            "failed_nodes": self.failed_nodes,
            "skipped_nodes": self.skipped_nodes,
            "blocked_nodes": self.blocked_nodes,
            "waiting_nodes": self.waiting_nodes,
        }

        for field_name, value in numeric_fields.items():
            if value < 0:
                raise ValueError(f"{field_name} cannot be negative")

        if not 0.0 <= self.success_rate <= 1.0:
            raise ValueError("success_rate must be between 0.0 and 1.0")


@dataclass(frozen=True)
class MonitorReport:
    pipeline_state: PipelineExecutionState
    nodes: list[NodeExecutionState]
    timeline: list[TimelineEvent]
    metrics: MonitorMetrics

    def __post_init__(self) -> None:
        if not isinstance(self.pipeline_state, PipelineExecutionState):
            raise TypeError("pipeline_state must be PipelineExecutionState")

        if not isinstance(self.metrics, MonitorMetrics):
            raise TypeError("metrics must be MonitorMetrics")

        for node in self.nodes:
            if not isinstance(node, NodeExecutionState):
                raise TypeError("nodes must contain NodeExecutionState items")

        for event in self.timeline:
            if not isinstance(event, TimelineEvent):
                raise TypeError("timeline must contain TimelineEvent items")
