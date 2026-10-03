from datetime import timedelta

from backend.app.models.security_event import SecurityEvent


class EventCorrelator:
    """
    Correlates security events that may belong
    to the same security investigation.
    """

    def __init__(self, time_window_minutes: int = 15):
        self.time_window = timedelta(minutes=time_window_minutes)

    def correlate(
        self,
        events: list[SecurityEvent],
    ) -> list[list[SecurityEvent]]:
        """
        Group related security events into investigations.
        """

        if not events:
            return []

        sorted_events = sorted(
            events,
            key=lambda event: event.timestamp
        )

        investigations: list[list[SecurityEvent]] = []

        for event in sorted_events:

            matching_investigation = None

            for investigation in investigations:

                if self._is_related(
                    event,
                    investigation
                ):
                    matching_investigation = investigation
                    break

            if matching_investigation:
                matching_investigation.append(event)
            else:
                investigations.append([event])

        return investigations

    def _is_related(
        self,
        event: SecurityEvent,
        investigation: list[SecurityEvent],
    ) -> bool:
        """
        Determine whether an event belongs to an
        existing investigation.
        """

        for existing_event in investigation:

            # 1. Same hostname
            if (
                event.hostname
                and existing_event.hostname
                and event.hostname == existing_event.hostname
            ):
                if self._within_time_window(
                    event,
                    existing_event
                ):
                    return True

            # 2. Same username
            if (
                event.username
                and existing_event.username
                and event.username == existing_event.username
            ):
                if self._within_time_window(
                    event,
                    existing_event
                ):
                    return True

            # 3. Same source IP
            if (
                event.source_ip
                and existing_event.source_ip
                and event.source_ip == existing_event.source_ip
            ):
                if self._within_time_window(
                    event,
                    existing_event
                ):
                    return True

        return False

    def _within_time_window(
        self,
        first: SecurityEvent,
        second: SecurityEvent,
    ) -> bool:
        """
        Check whether two events occurred close enough
        together to potentially belong to the same investigation.
        """

        difference = abs(
            first.timestamp - second.timestamp
        )

        return difference <= self.time_window