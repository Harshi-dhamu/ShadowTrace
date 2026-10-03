from backend.app.correlation.engine import EventCorrelator
from backend.app.ingestion.event_loader import load_events


def main():
    events = load_events(
        "data/raw/scenario_001.json"
    )

    correlator = EventCorrelator(
        time_window_minutes=15
    )

    investigations = correlator.correlate(events)

    print()
    print("=" * 60)
    print("SHADOWTRACE CORRELATION ENGINE")
    print("=" * 60)

    print(f"Total events: {len(events)}")
    print(
        f"Investigations created: "
        f"{len(investigations)}"
    )

    print()

    for index, investigation in enumerate(
        investigations,
        start=1
    ):
        print(
            f"Investigation #{index}"
        )

        print("-" * 40)

        for event in investigation:
            print(
                f"{event.timestamp} | "
                f"{event.event_type} | "
                f"{event.hostname} | "
                f"{event.username}"
            )

        print()


if __name__ == "__main__":
    main()