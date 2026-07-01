import pytest

from pipeline_execution_monitor.contract import TimelineEvent
from pipeline_execution_monitor.timeline import (
    build_timeline,
    get_timeline_summary,
    sort_timeline,
)


def test_build_timeline_from_execution_log():
    timeline = build_timeline(
        {
            "events": [
                {
                    "timestamp": "2026-07-01T20:00:00Z",
                    "event": "pipeline_started",
                    "message": "Pipeline started",
                },
                {
                    "timestamp": "2026-07-01T20:00:01Z",
                    "event": "node_started",
                    "node_id": "validate",
                    "message": "Node started",
                },
            ]
        }
    )

    assert len(timeline) == 2
    assert isinstance(timeline[0], TimelineEvent)
    assert timeline[0].event == "pipeline_started"
    assert timeline[1].node_id == "validate"


def test_build_timeline_sorts_by_timestamp():
    timeline = build_timeline(
        {
            "events": [
                {
                    "timestamp": "2026-07-01T20:00:03Z",
                    "event": "node_finished",
                    "node_id": "validate",
                },
                {
                    "timestamp": "2026-07-01T20:00:01Z",
                    "event": "node_started",
                    "node_id": "validate",
                },
            ]
        }
    )

    assert timeline[0].event == "node_started"
    assert timeline[1].event == "node_finished"


def test_build_timeline_accepts_empty_events():
    assert build_timeline({"events": []}) == []


def test_build_timeline_rejects_invalid_events_type():
    with pytest.raises(ValueError):
        build_timeline({"events": {}})


def test_build_timeline_rejects_non_object_event_item():
    with pytest.raises(ValueError):
        build_timeline({"events": ["bad-event"]})


def test_build_timeline_requires_timestamp():
    with pytest.raises(ValueError):
        build_timeline(
            {
                "events": [
                    {
                        "event": "node_started",
                    }
                ]
            }
        )


def test_build_timeline_requires_event():
    with pytest.raises(ValueError):
        build_timeline(
            {
                "events": [
                    {
                        "timestamp": "2026-07-01T20:00:01Z",
                    }
                ]
            }
        )


def test_sort_timeline_returns_sorted_copy():
    late = TimelineEvent(
        timestamp="2026-07-01T20:00:03Z",
        event="node_finished",
        node_id="validate",
    )
    early = TimelineEvent(
        timestamp="2026-07-01T20:00:01Z",
        event="node_started",
        node_id="validate",
    )

    timeline = [late, early]
    sorted_timeline = sort_timeline(timeline)

    assert sorted_timeline[0] == early
    assert sorted_timeline[1] == late
    assert timeline[0] == late


def test_get_timeline_summary():
    timeline = [
        TimelineEvent(
            timestamp="2026-07-01T20:00:00Z",
            event="pipeline_started",
        ),
        TimelineEvent(
            timestamp="2026-07-01T20:00:03Z",
            event="node_finished",
            node_id="validate",
        ),
    ]

    summary = get_timeline_summary(timeline)

    assert summary["total_events"] == 2
    assert summary["first_event"] == "pipeline_started"
    assert summary["last_event"] == "node_finished"
    assert summary["first_timestamp"] == "2026-07-01T20:00:00Z"
    assert summary["last_timestamp"] == "2026-07-01T20:00:03Z"


def test_get_timeline_summary_empty():
    summary = get_timeline_summary([])

    assert summary["total_events"] == 0
    assert summary["first_event"] is None
    assert summary["last_event"] is None
