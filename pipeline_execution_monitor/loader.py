import json
from pathlib import Path
from typing import Any


class ExecutionLogLoaderError(Exception):
    """Raised when an execution log cannot be loaded or normalized."""


def load_execution_log(file_path: str | Path) -> dict[str, Any]:
    path = Path(file_path)

    if not path.exists():
        raise ExecutionLogLoaderError(f"execution log file not found: {path}")

    if not path.is_file():
        raise ExecutionLogLoaderError(f"execution log path is not a file: {path}")

    try:
        with path.open("r", encoding="utf-8") as file:
            payload = json.load(file)
    except json.JSONDecodeError as error:
        raise ExecutionLogLoaderError(f"invalid execution log JSON: {error}") from error

    if not isinstance(payload, dict):
        raise ExecutionLogLoaderError("execution log root must be a JSON object")

    return normalize_execution_log(payload)


def normalize_execution_log(payload: dict[str, Any]) -> dict[str, Any]:
    pipeline_id = payload.get("pipeline_id") or payload.get("id")

    if not pipeline_id:
        raise ExecutionLogLoaderError("execution log requires pipeline_id")

    raw_nodes = payload.get("nodes", [])
    raw_events = payload.get("events", [])

    if raw_nodes is None:
        raw_nodes = []

    if raw_events is None:
        raw_events = []

    if not isinstance(raw_nodes, list):
        raise ExecutionLogLoaderError("execution log nodes must be a list")

    if not isinstance(raw_events, list):
        raise ExecutionLogLoaderError("execution log events must be a list")

    return {
        "pipeline_id": str(pipeline_id),
        "status": payload.get("status", "unknown"),
        "started_at": payload.get("started_at"),
        "finished_at": payload.get("finished_at"),
        "duration_seconds": payload.get("duration_seconds"),
        "nodes": raw_nodes,
        "events": raw_events,
        "metadata": payload.get("metadata", {}),
    }
