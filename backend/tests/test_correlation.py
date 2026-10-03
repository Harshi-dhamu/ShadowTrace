from datetime import datetime, timezone

from backend.app.correlation.engine import EventCorrelator
from backend.app.models.security_event import SecurityEvent


def create_event(
    event_id: str,
    event_type: str,
    timestamp: str,
    hostname: str = "WS-001",
    username: str = "analyst",
    source_ip: str = "10.10.20.45",
):
    return SecurityEvent(
        event_id=event_id,
        timestamp=datetime.fromisoformat(timestamp).replace(
            tzinfo=timezone.utc
        ),
        event_type=event_type,
        source="test",
        hostname=hostname,
        username=username,
        source_ip=source_ip,
        action=event_type.lower(),
        severity="medium",
    )


def test_related_events_are_correlated():
    events = [
        create_event(
            "evt-001",
            "LOGIN_FAILURE",
            "2026-10-01T08:42:11",
        ),
        create_event(
            "evt-002",
            "LOGIN_FAILURE",
            "2026-10-01T08:42:19",
        ),
        create_event(
            "evt-003",
            "LOGIN_SUCCESS",
            "2026-10-01T08:43:02",
        ),
    ]

    correlator = EventCorrelator()

    investigations = correlator.correlate(events)

    assert len(investigations) == 1
    assert len(investigations[0]) == 3


def test_unrelated_hosts_are_separated():
    events = [
        create_event(
            "evt-001",
            "LOGIN_FAILURE",
            "2026-10-01T08:42:11",
            hostname="WS-001",
            username="analyst",
            source_ip="10.10.20.45",
        ),
        create_event(
            "evt-002",
            "PROCESS_CREATED",
            "2026-10-01T08:43:00",
            hostname="WS-002",
            username="developer",
            source_ip="10.10.30.55",
        ),
    ]

    correlator = EventCorrelator()

    investigations = correlator.correlate(events)

    assert len(investigations) == 2


def test_events_outside_time_window_are_separated():
    events = [
        create_event(
            "evt-001",
            "LOGIN_FAILURE",
            "2026-10-01T08:42:11",
        ),
        create_event(
            "evt-002",
            "LOGIN_SUCCESS",
            "2026-10-01T09:30:00",
        ),
    ]

    correlator = EventCorrelator(
        time_window_minutes=15
    )

    investigations = correlator.correlate(events)

    assert len(investigations) == 2