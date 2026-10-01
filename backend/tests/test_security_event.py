from datetime import datetime, timezone

from backend.app.models.security_event import SecurityEvent


def test_security_event_creation():
    event = SecurityEvent(
        event_id="evt-0001",
        timestamp=datetime.now(timezone.utc),
        event_type="LOGIN_FAILURE",
        source="authentication",
        hostname="WS-001",
        username="analyst",
        source_ip="10.10.20.45",
        action="authentication_failed",
        severity="medium",
        metadata={
            "reason": "invalid_password"
        },
    )

    assert event.event_id == "evt-0001"
    assert event.event_type == "LOGIN_FAILURE"
    assert event.username == "analyst"
    assert event.severity == "medium"


def test_optional_fields_can_be_empty():
    event = SecurityEvent(
        event_id="evt-0002",
        timestamp=datetime.now(timezone.utc),
        event_type="LOGIN_SUCCESS",
        source="authentication",
    )

    assert event.hostname is None
    assert event.username is None
    assert event.source_ip is None
    assert event.metadata == {}