import json

import pytest

from pipeline_execution_monitor.loader import (
    ExecutionLogLoaderError,
    load_execution_log,
    normalize_execution_log,
)


def test_load_execution_log_from_file(tmp_path):
    log_file = tmp_path / "execution.json"
    log_file.write_text(
        json.dumps(
            {
                "pipeline_id": "pipeline-001",
                "status": "running",
                "nodes": [],
                "events": [],
            }
        ),
        encoding="utf-8",
    )

    payload = load_execution_log(log_file)

    assert payload["pipeline_id"] == "pipeline-001"
    assert payload["status"] == "running"
    assert payload["nodes"] == []
    assert payload["events"] == []


def test_load_execution_log_rejects_missing_file(tmp_path):
    missing_file = tmp_path / "missing.json"

    with pytest.raises(ExecutionLogLoaderError):
        load_execution_log(missing_file)


def test_load_execution_log_rejects_invalid_json(tmp_path):
    log_file = tmp_path / "bad.json"
    log_file.write_text("{bad-json", encoding="utf-8")

    with pytest.raises(ExecutionLogLoaderError):
        load_execution_log(log_file)


def test_load_execution_log_rejects_non_object_json(tmp_path):
    log_file = tmp_path / "list.json"
    log_file.write_text(json.dumps([]), encoding="utf-8")

    with pytest.raises(ExecutionLogLoaderError):
        load_execution_log(log_file)


def test_normalize_execution_log_accepts_id_alias():
    payload = normalize_execution_log(
        {
            "id": "pipeline-alias-001",
            "status": "completed",
        }
    )

    assert payload["pipeline_id"] == "pipeline-alias-001"
    assert payload["status"] == "completed"
    assert payload["nodes"] == []
    assert payload["events"] == []


def test_normalize_execution_log_rejects_missing_pipeline_id():
    with pytest.raises(ExecutionLogLoaderError):
        normalize_execution_log(
            {
                "status": "running",
                "nodes": [],
                "events": [],
            }
        )


def test_normalize_execution_log_rejects_invalid_nodes_type():
    with pytest.raises(ExecutionLogLoaderError):
        normalize_execution_log(
            {
                "pipeline_id": "pipeline-001",
                "nodes": {},
                "events": [],
            }
        )


def test_normalize_execution_log_rejects_invalid_events_type():
    with pytest.raises(ExecutionLogLoaderError):
        normalize_execution_log(
            {
                "pipeline_id": "pipeline-001",
                "nodes": [],
                "events": {},
            }
        )
