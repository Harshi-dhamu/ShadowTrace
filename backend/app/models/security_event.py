from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class SecurityEvent(BaseModel):
    """
    Standardized security event used throughout ShadowTrace.

    All incoming security data will eventually be converted
    into this common format before correlation and investigation.
    """

    event_id: str = Field(
        ...,
        description="Unique identifier for the security event"
    )

    timestamp: datetime = Field(
        ...,
        description="Time when the event occurred"
    )

    event_type: str = Field(
        ...,
        description="Type of security event"
    )

    source: str = Field(
        ...,
        description="System or subsystem that generated the event"
    )

    hostname: str | None = Field(
        default=None,
        description="Hostname or asset associated with the event"
    )

    username: str | None = Field(
        default=None,
        description="User associated with the event"
    )

    source_ip: str | None = Field(
        default=None,
        description="Source IP address"
    )

    destination_ip: str | None = Field(
        default=None,
        description="Destination IP address"
    )

    process: str | None = Field(
        default=None,
        description="Process involved in the event"
    )

    action: str | None = Field(
        default=None,
        description="Action performed during the event"
    )

    severity: str = Field(
        default="low",
        description="Event severity: low, medium, high, or critical"
    )

    metadata: dict[str, Any] = Field(
        default_factory=dict,
        description="Additional event-specific information"
    )