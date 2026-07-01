import json

from pipeline_execution_monitor.cli import main


def test_cli_prints_help_when_no_command(capsys):
    exit_code = main([])

    captured = capsys.readouterr()

    assert exit_code == 0
    assert "pipeline-monitor" in captured.out


def test_cli_monitor_outputs_summary(tmp_path, capsys):
    log_file = tmp_path / "execution.json"
    log_file.write_text(
        json.dumps(
            {
                "pipeline_id": "pipeline-001",
                "status": "running",
                "started_at": "2026-07-01T20:00:00Z",
                "duration_seconds": 12.5,
                "nodes": [
                    {
                        "node_id": "validate",
                        "node_name": "Validate Pipeline",
                        "status": "completed",
                    },
                    {
                        "node_id": "execute",
                        "node_name": "Execute Pipeline",
                        "status": "running",
                    },
                ],
                "events": [
                    {
                        "timestamp": "2026-07-01T20:00:00Z",
                        "event": "pipeline_started",
                    }
                ],
            }
        ),
        encoding="utf-8",
    )

    exit_code = main(["monitor", str(log_file)])

    captured = capsys.readouterr()

    assert exit_code == 0
    assert "Pipeline Execution Monitor" in captured.out
    assert "Pipeline ID: pipeline-001" in captured.out
    assert "Status: running" in captured.out
    assert "Total Nodes: 2" in captured.out
    assert "Completed Nodes: 1" in captured.out


def test_cli_monitor_verbose_outputs_nodes_and_timeline(tmp_path, capsys):
    log_file = tmp_path / "execution.json"
    log_file.write_text(
        json.dumps(
            {
                "pipeline_id": "pipeline-001",
                "status": "running",
                "nodes": [
                    {
                        "node_id": "validate",
                        "node_name": "Validate Pipeline",
                        "status": "completed",
                    }
                ],
                "events": [
                    {
                        "timestamp": "2026-07-01T20:00:00Z",
                        "event": "node_started",
                        "node_id": "validate",
                        "message": "Validation started",
                    }
                ],
            }
        ),
        encoding="utf-8",
    )

    exit_code = main(["monitor", str(log_file), "--verbose"])

    captured = capsys.readouterr()

    assert exit_code == 0
    assert "Nodes" in captured.out
    assert "validate | Validate Pipeline | completed" in captured.out
    assert "Timeline" in captured.out
    assert "node_started" in captured.out


def test_cli_monitor_returns_error_for_missing_file(capsys):
    exit_code = main(["monitor", "missing.json"])

    captured = capsys.readouterr()

    assert exit_code == 1
    assert "error:" in captured.err


def test_cli_monitor_json_writes_report(tmp_path, capsys):
    log_file = tmp_path / "execution.json"
    output_file = tmp_path / "monitor_report.json"

    log_file.write_text(
        json.dumps(
            {
                "pipeline_id": "pipeline-001",
                "status": "completed",
                "nodes": [
                    {
                        "node_id": "validate",
                        "node_name": "Validate Pipeline",
                        "status": "completed",
                    }
                ],
                "events": [
                    {
                        "timestamp": "2026-07-01T20:00:00Z",
                        "event": "pipeline_started",
                    }
                ],
            }
        ),
        encoding="utf-8",
    )

    exit_code = main(
        [
            "monitor",
            str(log_file),
            "--json",
            "--output",
            str(output_file),
        ]
    )

    captured = capsys.readouterr()

    assert exit_code == 0
    assert "JSON monitor report written:" in captured.out
    assert output_file.exists()

    payload = json.loads(output_file.read_text(encoding="utf-8"))

    assert payload["pipeline_state"]["pipeline_id"] == "pipeline-001"
    assert payload["metrics"]["total_nodes"] == 1
