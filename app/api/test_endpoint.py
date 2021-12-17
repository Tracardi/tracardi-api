from fastapi import APIRouter, Request

from app.config import server
from tracardi.domain.event_source import EventSource
from tracardi.service.storage.driver import storage

router = APIRouter()


@router.get("/test/resource", tags=["test"], include_in_schema=server.expose_gui_api)
async def create_test_data():
    resource = EventSource(
        id="@test-resource",
        type="web-page",
        name="Test resource",
        description="This resource is created for test purposes.",
    )
    return await storage.driver.event_source.save(resource)

