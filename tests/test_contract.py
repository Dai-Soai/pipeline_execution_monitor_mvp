import pytest

from pipeline_execution_monitor.contract import (
    MonitorMetrics,
    MonitorReport,
    NodeExecutionState,
    PipelineExecutionState,
    TimelineEvent,
)


def test_pipeline_execution_state_creation():
    state = PipelineExecutionState(
        pipeline_id="pipeline-001",
        status="running",
        started_at="2026-07-01T19:00:00Z",
    )

    assert state.pipeline_id == "pipeline-001"
    assert state.status == "running"
    assert state.started_at == "2026-07-01T19:00:00Z"


def test_pipeline_execution_state_rejects_invalid_status():
    with pytest.raises(ValueError):
        PipelineExecutionState(
            pipeline_id="pipeline-001",
            status="invalid",
        )


def test_node_execution_state_creation():
    node = NodeExecutionState(
        node_id="node-001",
        node_name="validate_pipeline",
        status="completed",
        duration_seconds=1.25,
    )

    assert node.node_id == "node-001"
    assert node.node_name == "validate_pipeline"
    assert node.status == "completed"
    assert node.duration_seconds == 1.25


def test_timeline_event_creation():
    event = TimelineEvent(
        timestamp="2026-07-01T19:01:00Z",
        event="node_started",
        node_id="node-001",
        message="Node started",
    )

    assert event.event == "node_started"
    assert event.node_id == "node-001"


def test_monitor_metrics_creation():
    metrics = MonitorMetrics(
        total_nodes=4,
        completed_nodes=3,
        running_nodes=1,
        success_rate=0.75,
        elapsed_seconds=12.5,
    )

    assert metrics.total_nodes == 4
    assert metrics.completed_nodes == 3
    assert metrics.success_rate == 0.75


def test_monitor_metrics_rejects_invalid_success_rate():
    with pytest.raises(ValueError):
        MonitorMetrics(
            total_nodes=1,
            success_rate=1.5,
        )


def test_monitor_report_creation():
    pipeline_state = PipelineExecutionState(
        pipeline_id="pipeline-001",
        status="running",
    )

    node = NodeExecutionState(
        node_id="node-001",
        node_name="validate_pipeline",
        status="completed",
    )

    event = TimelineEvent(
        timestamp="2026-07-01T19:01:00Z",
        event="node_finished",
        node_id="node-001",
    )

    metrics = MonitorMetrics(
        total_nodes=1,
        completed_nodes=1,
        success_rate=1.0,
    )

    report = MonitorReport(
        pipeline_state=pipeline_state,
        nodes=[node],
        timeline=[event],
        metrics=metrics,
    )

    assert report.pipeline_state.pipeline_id == "pipeline-001"
    assert len(report.nodes) == 1
    assert len(report.timeline) == 1
    assert report.metrics.completed_nodes == 1
