from pipeline_execution_monitor.contract import (
    MonitorMetrics,
    NodeExecutionState,
    PipelineExecutionState,
)


def build_metrics(
    nodes: list[NodeExecutionState],
    pipeline_state: PipelineExecutionState | None = None,
) -> MonitorMetrics:
    total_nodes = len(nodes)

    completed_nodes = count_nodes_by_status(nodes, "completed")
    running_nodes = count_nodes_by_status(nodes, "running")
    failed_nodes = count_nodes_by_status(nodes, "failed")
    skipped_nodes = count_nodes_by_status(nodes, "skipped")
    blocked_nodes = count_nodes_by_status(nodes, "blocked")
    waiting_nodes = count_nodes_by_status(nodes, "waiting")

    success_rate = calculate_success_rate(
        completed_nodes=completed_nodes,
        total_nodes=total_nodes,
    )

    elapsed_seconds = None
    if pipeline_state is not None:
        elapsed_seconds = pipeline_state.duration_seconds

    return MonitorMetrics(
        total_nodes=total_nodes,
        completed_nodes=completed_nodes,
        running_nodes=running_nodes,
        failed_nodes=failed_nodes,
        skipped_nodes=skipped_nodes,
        blocked_nodes=blocked_nodes,
        waiting_nodes=waiting_nodes,
        success_rate=success_rate,
        elapsed_seconds=elapsed_seconds,
    )


def count_nodes_by_status(
    nodes: list[NodeExecutionState],
    status: str,
) -> int:
    return sum(1 for node in nodes if node.status == status)


def calculate_success_rate(
    completed_nodes: int,
    total_nodes: int,
) -> float:
    if total_nodes == 0:
        return 0.0

    return completed_nodes / total_nodes
