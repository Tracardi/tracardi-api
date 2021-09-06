from time import sleep

from fastapi import APIRouter, Depends
from fastapi import HTTPException
from tracardi.service.storage.factory import StorageFor, StorageForBulk

from tracardi.domain.record.event_debug_record import EventDebugRecord
from tracardi_graph_runner.domain.debug_info import DebugInfo
from .auth.authentication import get_current_user
from tracardi.domain.entity import Entity
from tracardi.event_server.service.persistence_service import PersistenceService
from tracardi.service.storage.elastic_storage import ElasticStorage
from tracardi.domain.event import Event
from tracardi.domain.profile import Profile

router = APIRouter(
    dependencies=[Depends(get_current_user)]
)


@router.get("/events/metadata/type", tags=["event", "event server"])
async def event_types():
    result = await StorageForBulk().index('event').uniq_field_value("type")
    return {
        "total": result.total,
        "result": list(result)
    }


@router.get("/event/{id}", tags=["event", "event server"])
async def get_event(id: str):
    try:
        event = Entity(id=id)
        # Loads TrackerPayload as it has broader data
        full_event = await StorageFor(event).index("event").load(Event)  # type: Event
        if full_event is None:
            raise HTTPException(detail="Event {} does not exist.".format(id), status_code=404)

        profile = Entity(id=full_event.profile.id)
        full_event.profile = await StorageFor(profile).index("profile").load(Profile)

        query = {
            "query": {
                "match": {
                    "events.ids": id,
                }
            }
        }

        index = PersistenceService(ElasticStorage(index_key="stat-log"))
        event_result = await index.filter(query)

        return {
            "event": full_event,
            "result": list(event_result)[0] if event_result.total == 1 else None
        }

    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/event/{id}", tags=["event", "event server"])
async def delete_event(id: str):
    try:
        event = Entity(id=id)
        return await StorageFor(event).index("event").delete()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/event/debug/{id}", tags=["event", "event server"], response_model=DebugInfo)
async def get_event_debug_info(id: str):
    debug_record = EventDebugRecord(id=id)
    encoded_debug_record = await StorageFor(debug_record).index().load()
    # encoded_debug_record = await debug_record.storage().load()
    if encoded_debug_record is not None:
        debug_info = EventDebugRecord.decode(encoded_debug_record)  # type: DebugInfo
        return debug_info
    return None
