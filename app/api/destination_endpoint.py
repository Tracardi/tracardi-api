from fastapi import APIRouter, Response, HTTPException, Depends
from tracardi.service.storage.driver import storage
from tracardi.domain.destination import Destination, DestinationRecord
from .auth.authentication import get_current_user
from ..config import server
from ..service.grouping import group_records

router = APIRouter(
    dependencies=[Depends(get_current_user)]
)


@router.post("/destination", tags=["destination"], response_model=dict,
             include_in_schema=server.expose_gui_api)
async def save_destination(destination: Destination):

    """
    Upserts destination data.
    """

    try:
        record = DestinationRecord.encode(destination)
        result = await storage.driver.destination.save(record)
        await storage.driver.destination.refresh()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/destination/{id}", tags=["destination"], response_model=Destination,
            include_in_schema=server.expose_gui_api)
async def get_destination(id: str, response: Response):

    """
    Returns destination or None if destination does not exist.
    """

    try:
        destination_record = await storage.driver.destination.load(id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    if destination_record is None:
        response.status_code = 404
        return None

    return destination_record.decode()


@router.get("/destinations", tags=["destination"], response_model=dict,
            include_in_schema=server.expose_gui_api)
async def get_destinations():

    """
    Returns destinations.
    """

    try:
        storage_result = await storage.driver.destination.load_all()
        return {
            "total": storage_result.total,
            "result": list(storage_result)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/destinations/by_tag", tags=["destination"], response_model=dict, include_in_schema=server.expose_gui_api)
async def get_destinations_by_tag(query: str = None, start: int = 0, limit: int = 100) -> dict:
    try:
        result = await storage.driver.destination.load_all(start, limit=limit)
        return group_records(result, query, group_by='tags', search_by='name', sort_by='name')
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/destination/{id}", tags=["destination"], include_in_schema=server.expose_gui_api)
async def delete_destination(id: str, response: Response):
    try:
        result = await storage.driver.destination.delete(id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    if result is None:
        response.status_code = 404
        return None

    try:
        await storage.driver.destination.refresh()
        return True
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
