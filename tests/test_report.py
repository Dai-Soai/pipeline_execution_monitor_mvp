import json

from pipeline_execution_monitor.contract import MonitorReport
from pipeline_execution_monitor.report import (
    build_monitor_report,
    build_monitor_report_from_file,
    monitor_report_to_dict,
    write_monitor_report_json,
)


def sample_execution_log():
    return {
        "pipeline_id": "pipeline-001",
        "status": "completed",
        "started_at": "2026-07-01T20:00:00Z",
        "finished_at": "2026-07-01T20:00:05Z",
        "duration_seconds": 5.0,
        "nodes": [
            {
                "node_id": "validate",
                "node_name": "Validate Pipeline",
                "status": "completed",
                "duration_seconds": 2.0,
            },
            {
                "node_id": "execute",
                "node_name": "Execute Pipeline",
                "status": "completed",
                "duration_seconds": 3.0,
            },
        ],
        "events": [
            {
                "timestamp": "2026-07-01T20:00:00Z",
                "event": "pipeline_started",
            },
            {
                "timestamp": "2026-07-01T20:00:05Z",
                "event": "pipeline_finished",
            },
        ],
    }


def test_build_monitor_report():
    report = build_monitor_report(sample_execution_log())

    assert isinstance(report, MonitorReport)
    assert report.pipeline_state.pipeline_id == "pipeline-001"
    assert report.pipeline_state.status == "completed"
    assert len(report.nodes) == 2
    assert len(report.timeline) == 2
    assert report.metrics.total_nodes == 2
    assert report.metrics.completed_nodes == 2
    assert report.metrics.success_rate == 1.0


def test_monitor_report_to_dict():
    report = build_monitor_report(sample_execution_log())
    payload = monitor_report_to_dict(report)

    assert payload["pipeline_state"]["pipeline_id"] == "pipeline-001"
    assert payload["metrics"]["total_nodes"] == 2
    assert payload["nodes"][0]["node_id"] == "validate"
    assert payload["timeline"][0]["event"] == "pipeline_started"


def test_write_monitor_report_json(tmp_path):
    report = build_monitor_report(sample_execution_log())
    output_file = tmp_path / "monitor_report.json"

    written_path = write_monitor_report_json(report, output_file)

    assert written_path == output_file
    assert output_file.exists()

    payload = json.loads(output_file.read_text(encoding="utf-8"))

    assert payload["pipeline_state"]["pipeline_id"] == "pipeline-001"
    assert payload["metrics"]["success_rate"] == 1.0


def test_build_monitor_report_from_file(tmp_path):
    log_file = tmp_path / "execution.json"
    log_file.write_text(
        json.dumps(sample_execution_log()),
        encoding="utf-8",
    )

    report = build_monitor_report_from_file(log_file)

    assert report.pipeline_state.pipeline_id == "pipeline-001"
    assert report.metrics.total_nodes == 2
