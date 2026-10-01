from backend.app.ingestion.event_loader import load_events


def test_load_attack_scenario():
    events = load_events("data/raw/scenario_001.json")

    assert len(events) == 9

    assert events[0].event_type == "LOGIN_FAILURE"
    assert events[3].event_type == "LOGIN_SUCCESS"
    assert events[4].event_type == "PROCESS_CREATED"
    assert events[-1].event_type == "FILE_ACCESS"


def test_events_are_loaded_as_security_events():
    events = load_events("data/raw/scenario_001.json")

    assert events[0].event_id == "evt-0001"
    assert events[0].username == "analyst"
    assert events[0].hostname == "WS-001"