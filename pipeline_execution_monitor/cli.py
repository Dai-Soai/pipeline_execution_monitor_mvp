import argparse
import sys

from pipeline_execution_monitor.loader import (
    ExecutionLogLoaderError,
    load_execution_log,
)
from pipeline_execution_monitor.metrics import build_metrics
from pipeline_execution_monitor.state_builder import (
    build_node_states,
    build_pipeline_state,
)
from pipeline_execution_monitor.timeline import (
    build_timeline,
    get_timeline_summary,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="pipeline-monitor",
        description="Observe pipeline execution status, timeline, node states, and metrics.",
    )

    subparsers = parser.add_subparsers(dest="command")

    monitor_parser = subparsers.add_parser(
        "monitor",
        help="Monitor a pipeline execution log.",
    )
    monitor_parser.add_argument(
        "execution_log",
        help="Path to execution log JSON file.",
    )
    monitor_parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show node states and timeline events.",
    )

    return parser


def run_monitor(args: argparse.Namespace) -> int:
    try:
        execution_log = load_execution_log(args.execution_log)
        pipeline_state = build_pipeline_state(execution_log)
        nodes = build_node_states(execution_log)
        timeline = build_timeline(execution_log)
        metrics = build_metrics(nodes, pipeline_state=pipeline_state)
        timeline_summary = get_timeline_summary(timeline)
    except (ExecutionLogLoaderError, ValueError, TypeError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1

    print("Pipeline Execution Monitor")
    print("==========================")
    print(f"Pipeline ID: {pipeline_state.pipeline_id}")
    print(f"Status: {pipeline_state.status}")
    print(f"Started At: {pipeline_state.started_at}")
    print(f"Finished At: {pipeline_state.finished_at}")
    print(f"Duration Seconds: {pipeline_state.duration_seconds}")
    print()
    print("Metrics")
    print("-------")
    print(f"Total Nodes: {metrics.total_nodes}")
    print(f"Completed Nodes: {metrics.completed_nodes}")
    print(f"Running Nodes: {metrics.running_nodes}")
    print(f"Failed Nodes: {metrics.failed_nodes}")
    print(f"Skipped Nodes: {metrics.skipped_nodes}")
    print(f"Blocked Nodes: {metrics.blocked_nodes}")
    print(f"Waiting Nodes: {metrics.waiting_nodes}")
    print(f"Success Rate: {metrics.success_rate:.2f}")
    print(f"Elapsed Seconds: {metrics.elapsed_seconds}")
    print()
    print("Timeline Summary")
    print("----------------")
    print(f"Total Events: {timeline_summary['total_events']}")
    print(f"First Event: {timeline_summary['first_event']}")
    print(f"Last Event: {timeline_summary['last_event']}")

    if args.verbose:
        print()
        print("Nodes")
        print("-----")
        for node in nodes:
            print(
                f"- {node.node_id} | {node.node_name} | "
                f"{node.status} | duration={node.duration_seconds}"
            )

        print()
        print("Timeline")
        print("--------")
        for event in timeline:
            node_part = f" | node={event.node_id}" if event.node_id else ""
            message_part = f" | {event.message}" if event.message else ""
            print(f"- {event.timestamp} | {event.event}{node_part}{message_part}")

    return 0


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "monitor":
        return run_monitor(args)

    parser.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
