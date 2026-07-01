import json
from dataclasses import asdict
from pathlib import Path
from typing import Any

from pipeline_execution_monitor.contract import MonitorReport
from pipeline_execution_monitor.loader import load_execution_log
from pipeline_execution_monitor.metrics import build_metrics
from pipeline_execution_monitor.state_builder import (
    build_node_states,
    build_pipeline_state,
)
from pipeline_execution_monitor.timeline import build_timeline


def build_monitor_report(execution_log: dict[str, Any]) -> MonitorReport:
    pipeline_state = build_pipeline_state(execution_log)
    nodes = build_node_states(execution_log)
    timeline = build_timeline(execution_log)
    metrics = build_metrics(nodes, pipeline_state=pipeline_state)

    return MonitorReport(
        pipeline_state=pipeline_state,
        nodes=nodes,
        timeline=timeline,
        metrics=metrics,
    )


def build_monitor_report_from_file(file_path: str | Path) -> MonitorReport:
    execution_log = load_execution_log(file_path)
    return build_monitor_report(execution_log)


def monitor_report_to_dict(report: MonitorReport) -> dict[str, Any]:
    return asdict(report)


def write_monitor_report_json(
    report: MonitorReport,
    output_path: str | Path,
) -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    payload = monitor_report_to_dict(report)

    path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    return path
