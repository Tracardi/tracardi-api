from datetime import datetime
from typing import Dict, Optional, Union

from cron_validator import CronValidator
from pydantic import BaseModel, validator
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

    @validator("name")
    def name_must_not_be_emtpy(cls, value):
        value = value.strip()
        if value == "":
            raise ValueError("Name must not be empty.")
        return value

    @validator("time")
    def time_must_not_be_emtpy(cls, value):
        value = value.strip()
        if CronValidator.parse(value) is None:
            raise ValueError("Cron time is invalid.")
        return value
