import json
from pathlib import Path

from backend.app.models.security_event import SecurityEvent


def load_events(file_path: str | Path) -> list[SecurityEvent]:
    """
    Load raw security events from a JSON file
    and convert them into SecurityEvent objects.
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Event file not found: {path}")

    with path.open("r", encoding="utf-8") as file:
        raw_events = json.load(file)

    if not isinstance(raw_events, list):
        raise ValueError("Event file must contain a JSON list")

    events = [
        SecurityEvent.model_validate(event)
        for event in raw_events
    ]

    return events