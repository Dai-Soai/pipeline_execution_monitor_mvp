from typing import Any

from pipeline_execution_monitor.contract import (
    NodeExecutionState,
    PipelineExecutionState,
)


STATUS_PRIORITY = [
    "failed",
    "blocked",
    "running",
    "waiting",
    "completed",
    "skipped",
    "unknown",
]


def build_pipeline_state(execution_log: dict[str, Any]) -> PipelineExecutionState:
    pipeline_id = execution_log.get("pipeline_id")
    if not pipeline_id:
        raise ValueError("execution_log requires pipeline_id")

    status = execution_log.get("status") or infer_pipeline_status(
        execution_log.get("nodes", [])
    )

    return PipelineExecutionState(
        pipeline_id=str(pipeline_id),
        status=status,
        started_at=execution_log.get("started_at"),
        finished_at=execution_log.get("finished_at"),
        duration_seconds=execution_log.get("duration_seconds"),
    )


def build_node_states(execution_log: dict[str, Any]) -> list[NodeExecutionState]:
    raw_nodes = execution_log.get("nodes", [])

    if raw_nodes is None:
        raw_nodes = []

    if not isinstance(raw_nodes, list):
        raise ValueError("execution_log nodes must be a list")

    nodes: list[NodeExecutionState] = []

    for index, raw_node in enumerate(raw_nodes):
        if not isinstance(raw_node, dict):
            raise ValueError("node item must be an object")

        node_id = raw_node.get("node_id") or raw_node.get("id")
        node_name = raw_node.get("node_name") or raw_node.get("name") or node_id

        if not node_id:
            raise ValueError(f"node at index {index} requires node_id")

        nodes.append(
            NodeExecutionState(
                node_id=str(node_id),
                node_name=str(node_name),
                status=raw_node.get("status", "unknown"),
                started_at=raw_node.get("started_at"),
                finished_at=raw_node.get("finished_at"),
                duration_seconds=raw_node.get("duration_seconds"),
                metadata=raw_node.get("metadata", {}),
            )
        )

    return nodes


def infer_pipeline_status(raw_nodes: list[dict[str, Any]]) -> str:
    if not raw_nodes:
        return "unknown"

    statuses = []

    for raw_node in raw_nodes:
        if isinstance(raw_node, dict):
            statuses.append(raw_node.get("status", "unknown"))
        else:
            statuses.append("unknown")

    if "failed" in statuses:
        return "failed"

    if "blocked" in statuses:
        return "blocked"

    if "running" in statuses:
        return "running"

    if "waiting" in statuses:
        return "waiting"

    if statuses and all(status == "completed" for status in statuses):
        return "completed"

    if statuses and all(status == "skipped" for status in statuses):
        return "skipped"

    return "unknown"


def build_execution_state(
    execution_log: dict[str, Any],
) -> tuple[
    PipelineExecutionState,
    list[NodeExecutionState],
]:
    return build_pipeline_state(execution_log), build_node_states(execution_log)
