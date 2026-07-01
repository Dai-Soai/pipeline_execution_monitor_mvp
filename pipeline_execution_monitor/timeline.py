from typing import Any

from pipeline_execution_monitor.contract import TimelineEvent


def build_timeline(execution_log: dict[str, Any]) -> list[TimelineEvent]:
    raw_events = execution_log.get("events", [])

    if raw_events is None:
        raw_events = []

    if not isinstance(raw_events, list):
        raise ValueError("execution_log events must be a list")

    timeline: list[TimelineEvent] = []

    for index, raw_event in enumerate(raw_events):
        if not isinstance(raw_event, dict):
            raise ValueError("timeline event item must be an object")

        timestamp = raw_event.get("timestamp")
        event = raw_event.get("event")

        if not timestamp:
            raise ValueError(f"timeline event at index {index} requires timestamp")

        if not event:
            raise ValueError(f"timeline event at index {index} requires event")

        timeline.append(
            TimelineEvent(
                timestamp=str(timestamp),
                event=str(event),
                node_id=raw_event.get("node_id"),
                message=raw_event.get("message"),
                metadata=raw_event.get("metadata", {}),
            )
        )

    return sort_timeline(timeline)


def sort_timeline(timeline: list[TimelineEvent]) -> list[TimelineEvent]:
    return sorted(timeline, key=lambda event: event.timestamp)


def get_timeline_summary(timeline: list[TimelineEvent]) -> dict[str, Any]:
    return {
        "total_events": len(timeline),
        "first_event": timeline[0].event if timeline else None,
        "last_event": timeline[-1].event if timeline else None,
        "first_timestamp": timeline[0].timestamp if timeline else None,
        "last_timestamp": timeline[-1].timestamp if timeline else None,
    }
