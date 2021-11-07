from typing import Dict, Optional

from pydantic import BaseModel
from tracardi.domain.entity import Entity
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
