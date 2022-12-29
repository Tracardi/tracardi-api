from datetime import datetime
from typing import Dict, Optional, Union

from pydantic import BaseModel
from tracardi.domain.entity import Entity
from tracardi.domain.payload.tracker_payload import TrackerPayload
from tracardi.domain.schedule import Schedule


class EventProperties(BaseModel):
    type: str
    properties: Dict = {}


class ScheduleData(BaseModel):
    schedule: Schedule
    event: EventProperties
    source: Entity
    profile: Entity
    session: Optional[Entity] = None
    context: Optional[Entity] = None


class Job(BaseModel):
    name: str
    description: Optional[str] = ""
    time: Union[datetime, str]
    tracker_payload: TrackerPayload
