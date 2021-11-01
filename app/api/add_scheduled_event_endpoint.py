from datetime import datetime
from fastapi import APIRouter
from tracardi.service.storage.drivers.elastic import raw
from typing import Dict, Union, List
from app.config import server
from pydantic import BaseModel, ValidationError
from pytimeparse.timeparse import timeparse


class Source(BaseModel):
    id: str


class Event(BaseModel):
    type: str
    properties: Dict = {"prop1": 1}


class Schedule(BaseModel):
    type: str = "date|delta|interval"
    time: Union[str, List[str]] = datetime.utcnow()

    def get_parsed_time(self):
        if self.type == "date":
            return datetime.strptime(self.time, "%Y-%m-%dT%H:%M:%S.%f").timestamp()
        elif self.type == "delta":
            return timeparse(self.time)
        elif self.type == "interval":
            return (datetime.strptime(self.time[0], "%Y-%m-%dT%H:%M:%S.%f").timestamp(),
                    datetime.strptime(self.time[1], "%Y-%m-%dT%H:%M:%S.%f").timestamp())
        else:
            raise ValidationError("Type should take value of 'date', 'delta' or 'interval'.")


class EventForm(BaseModel):
    source: Source
    event: Event
    schedule: Schedule


router = APIRouter()


@router.post("/event/schedule", tags=["event"], include_in_schema=server.expose_gui_api)
async def add_scheduled_event(inserted_event: EventForm):
    result = await raw.index("task").storage.create([{
        "timestamp": inserted_event.schedule.get_parsed_time(),
        "event": {
            "metadata": {
                "time": {
                    "insert": datetime.utcnow()
                }
            },
            "type": inserted_event.event.type,
            "properties": inserted_event.event.properties,
            "context": {"No context data provided.": None},
            "session": {
                "id": None
            },
            "source": {
                "id": inserted_event.source.id
            },
            "profile": {
                "id": None
            }
        },
        "status": None
    }])
    return {"result": result.errors if result.errors else "OK"}
