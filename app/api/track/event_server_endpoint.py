import logging

from fastapi import APIRouter, Request
from fastapi import HTTPException

from app.api.track.service.tracker import track_event
from tracardi.domain.payload.tracker_payload import TrackerPayload
from tracardi.exceptions.exception import TracardiException

logger = logging.getLogger('tracardi.api.event_server')

router = APIRouter()


@router.post("/track", tags=['tracker'])
async def track(tracker_payload: TrackerPayload, request: Request):
    try:
        return await track_event(tracker_payload, ip=request.client.host)
    except TracardiException as e:
        logger.error(str(e))
        raise HTTPException(detail=str(e), status_code=500)
