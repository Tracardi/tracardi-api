from fastapi import APIRouter
import tracardi.data.initial_data
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
        tags=['test']
    )
    return await storage.driver.event_source.save(resource)


@router.get("/test/data", tags=["test"], include_in_schema=server.expose_gui_api)
async def make_fake_data():
    for index, data in tracardi.data.initial_data.generate_fake_data().items():
        for record in data:
            record = record.dict()
            if index in ['event', 'session']:
                record['metadata']['time']['insert'] = tracardi.data.initial_data.generate_random_date()
            await storage.driver.raw.index(index).upsert(record)
