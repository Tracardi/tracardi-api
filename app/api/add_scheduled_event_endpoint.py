from datetime import datetime
from fastapi import APIRouter
from tracardi.service.storage.drivers.elastic import task
from typing import Dict
from app.config import server
from pydantic import BaseModel, validator
from pytimeparse.timeparse import timeparse


class Source(BaseModel):
    id: str


class Event(BaseModel):
    type: str
    properties: Dict = {}


class Schedule(BaseModel):
    type: str = "date|delta|interval"
    time: str = datetime.utcnow()

    @validator("type")
    def _validate_type(cls, value):
        if value not in ("delta", "date", "interval"):
            raise ValueError("'type' field must contain 'date', 'delta' or 'interval'.")
        return value

    @validator("time")
    def _validate_time(cls, value, values):
        if values["type"] in ("delta", "interval") and timeparse(value) is None:
            raise ValueError("value of 'time' is invalid according to type '{}'".format(values["type"]))
        else:
            datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f")
        return value

    def get_parsed_time(self):
        if self.type in ["interval", "delta"]:
            return timeparse(self.time)
        elif self.type == "date":
            return datetime.strptime(self.time, "%Y-%m-%dT%H:%M:%S.%f").timestamp()


class EventForm(BaseModel):
    source: Source
    event: Event
    schedule: Schedule


router = APIRouter()


@router.post("/event/schedule", tags=["event"], include_in_schema=server.expose_gui_api)
async def add_scheduled_event(inserted_event: EventForm):
    result = await task.create(
        timestamp=inserted_event.schedule.get_parsed_time(),
        type=inserted_event.event.type,
        properties=inserted_event.event.properties,
        context=None,
        session_id=None,
        source_id=inserted_event.source.id,
        profile_id=None,
        status=None
    )
    return {"result": result.errors if result.errors else "OK"}
