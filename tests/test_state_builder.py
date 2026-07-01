import pytest

from pipeline_execution_monitor.contract import (
    NodeExecutionState,
    PipelineExecutionState,
)
from pipeline_execution_monitor.state_builder import (
    build_execution_state,
    build_node_states,
    build_pipeline_state,
    infer_pipeline_status,
)


def test_build_pipeline_state_from_execution_log():
    state = build_pipeline_state(
        {
            "pipeline_id": "pipeline-001",
            "status": "running",
            "started_at": "2026-07-01T20:00:00Z",
            "duration_seconds": 10.5,
        }
    )

    assert isinstance(state, PipelineExecutionState)
    assert state.pipeline_id == "pipeline-001"
    assert state.status == "running"
    assert state.duration_seconds == 10.5


def test_build_pipeline_state_requires_pipeline_id():
    with pytest.raises(ValueError):
        build_pipeline_state(
            {
                "status": "running",
            }
        )


def test_build_node_states_from_execution_log():
    nodes = build_node_states(
        {
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
                    "status": "running",
                },
            ]
        }
    )

    assert len(nodes) == 2
    assert isinstance(nodes[0], NodeExecutionState)
    assert nodes[0].node_id == "validate"
    assert nodes[0].status == "completed"
    assert nodes[1].status == "running"


def test_build_node_states_accepts_id_and_name_aliases():
    nodes = build_node_states(
        {
            "nodes": [
                {
                    "id": "node-alias",
                    "name": "Alias Node",
                    "status": "completed",
                }
            ]
        }
    )

    assert nodes[0].node_id == "node-alias"
    assert nodes[0].node_name == "Alias Node"


def test_build_node_states_requires_node_id():
    with pytest.raises(ValueError):
        build_node_states(
            {
                "nodes": [
                    {
                        "node_name": "Broken Node",
                        "status": "failed",
                    }
                ]
            }
        )


def test_infer_pipeline_status_failed_has_priority():
    status = infer_pipeline_status(
        [
            {"status": "completed"},
            {"status": "failed"},
            {"status": "running"},
        ]
    )

    assert status == "failed"


def test_infer_pipeline_status_completed_when_all_completed():
    status = infer_pipeline_status(
        [
            {"status": "completed"},
            {"status": "completed"},
        ]
    )

    assert status == "completed"


def test_infer_pipeline_status_running_when_any_running():
    status = infer_pipeline_status(
        [
            {"status": "completed"},
            {"status": "running"},
        ]
    )

    assert status == "running"


def test_infer_pipeline_status_unknown_when_no_nodes():
    assert infer_pipeline_status([]) == "unknown"


def test_build_execution_state_returns_pipeline_and_nodes():
    pipeline_state, nodes = build_execution_state(
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
        }
    )

    assert pipeline_state.pipeline_id == "pipeline-001"
    assert len(nodes) == 1
    assert nodes[0].node_id == "validate"
