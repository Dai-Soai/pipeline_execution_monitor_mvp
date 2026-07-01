from pipeline_execution_monitor.contract import (
    NodeExecutionState,
    PipelineExecutionState,
)
from pipeline_execution_monitor.metrics import (
    build_metrics,
    calculate_success_rate,
    count_nodes_by_status,
)


def make_node(node_id: str, status: str) -> NodeExecutionState:
    return NodeExecutionState(
        node_id=node_id,
        node_name=node_id,
        status=status,
    )


def test_count_nodes_by_status():
    nodes = [
        make_node("a", "completed"),
        make_node("b", "completed"),
        make_node("c", "failed"),
    ]

    assert count_nodes_by_status(nodes, "completed") == 2
    assert count_nodes_by_status(nodes, "failed") == 1
    assert count_nodes_by_status(nodes, "running") == 0


def test_calculate_success_rate():
    assert calculate_success_rate(completed_nodes=3, total_nodes=4) == 0.75


def test_calculate_success_rate_returns_zero_when_no_nodes():
    assert calculate_success_rate(completed_nodes=0, total_nodes=0) == 0.0


def test_build_metrics_counts_all_statuses():
    nodes = [
        make_node("completed", "completed"),
        make_node("running", "running"),
        make_node("failed", "failed"),
        make_node("skipped", "skipped"),
        make_node("blocked", "blocked"),
        make_node("waiting", "waiting"),
    ]

    metrics = build_metrics(nodes)

    assert metrics.total_nodes == 6
    assert metrics.completed_nodes == 1
    assert metrics.running_nodes == 1
    assert metrics.failed_nodes == 1
    assert metrics.skipped_nodes == 1
    assert metrics.blocked_nodes == 1
    assert metrics.waiting_nodes == 1
    assert metrics.success_rate == 1 / 6


def test_build_metrics_uses_pipeline_duration_as_elapsed_seconds():
    nodes = [
        make_node("a", "completed"),
        make_node("b", "completed"),
    ]

    pipeline_state = PipelineExecutionState(
        pipeline_id="pipeline-001",
        status="completed",
        duration_seconds=12.5,
    )

    metrics = build_metrics(nodes, pipeline_state=pipeline_state)

    assert metrics.elapsed_seconds == 12.5


def test_build_metrics_handles_empty_nodes():
    metrics = build_metrics([])

    assert metrics.total_nodes == 0
    assert metrics.completed_nodes == 0
    assert metrics.success_rate == 0.0
