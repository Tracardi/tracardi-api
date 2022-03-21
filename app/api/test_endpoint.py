import asyncio

from fastapi import APIRouter, Depends
from app.api.auth.permissions import Permissions
from app.config import server
from app.service.data_generator import generate_fake_data, generate_random_date
from tracardi.domain.event_source import EventSource
from tracardi.service.storage.driver import storage

router = APIRouter(
    dependencies=[Depends(Permissions(roles=["admin"]))]
)


@router.get("/test/resource", tags=["test"], include_in_schema=server.expose_gui_api)
async def create_test_data():
    """
    Creates test resource data and saves it to database. Accessible for roles: "admin"
    """
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
    """
    Creates fake data and saves it to database. Accessible for roles: "admin"
    """
    for index, data in generate_fake_data().items():
        for record in data:
            record = record.dict()
            if index in ['event', 'session']:
                record['metadata']['time']['insert'] = generate_random_date()
            await storage.driver.raw.index(index).upsert(record)

