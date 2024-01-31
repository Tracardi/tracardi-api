from fastapi import APIRouter, Depends
from tracardi.exceptions.log_handler import get_logger
from tracardi.service.events import get_predefined_event_types, \
    get_default_event_type_schema
from .auth.permissions import Permissions
from tracardi.config import tracardi

logger = get_logger(__name__)

router = APIRouter(
    dependencies=[Depends(Permissions(roles=["admin", "developer"]))]
)


@router.get("/event-type/build-in/{id}",
            tags=["event-type"],
            include_in_schema=tracardi.expose_gui_api)
async def get_build_in_event_type(id: str = None):
    return get_default_event_type_schema(event_type=id)


@router.get("/event-types/build-in/by_type",
            tags=["event-type"],
            include_in_schema=tracardi.expose_gui_api)
async def list_build_in_event_types(query: str = None):
    """
    Lists all build-in event types
    """
    result = get_predefined_event_types()

    total = len(result)

    # Filtering
    if query is not None and len(query) > 0:
        query = query.lower()
        if query:
            result = [{"id": definition['id'], "name": definition['name'], "description": definition['description']} for
                      _, definition in result if
                      query in definition['name'].lower() or query in definition['description'].lower()]
    else:
        result = [{"id": definition['id'], "name": definition['name'], "description": definition['description']} for
                  _, definition in result]

    return {
        "total": total,
        "grouped": {
            "Build In": result
        }
    }
