import json
from collections import defaultdict
from urllib.parse import urljoin, urlparse

from aiohttp import InvalidURL, ClientError
from fastapi import APIRouter
from fastapi import HTTPException, Depends, Response, status
from tracardi.domain.credentials import Credentials
from tracardi.service.microservice import MicroserviceApi
from tracardi.domain.named_entity import NamedEntity
from tracardi.domain.enum.type_enum import TypeEnum
from tracardi.domain.event_source import EventSource
from tracardi.service.storage.driver import storage
from .auth.authentication import get_current_user
from .grouper import search
from ..config import server

router = APIRouter(
    dependencies=[Depends(get_current_user)]
)


def event_source_types():
    return {
        "tracardi-pro": {
            "tags": ['pro', 'api'],
            "name": "Tracardi Pro Service",
            "configurable": True
        },
        "web-page": {
            "tags": ['web-page', "input", "output"],
            "name": "Web page",
            "configurable": False
        }
    }


@router.get("/event-sources/by_type",
            tags=["event-source"],
            include_in_schema=server.expose_gui_api)
async def list_resources(query: str = None):
    try:

        result, total = await storage.driver.event_source.load_all()

        # Filtering
        if query is not None and len(query) > 0:
            query = query.lower()
            if query:
                result = [r for r in result if query in r.name.lower() or search(query, r.type)]

        # Grouping
        groups = defaultdict(list)
        for event_source in result:  # type: EventSource
            if isinstance(event_source.type, list):
                for group in event_source.type:
                    groups[group].append(event_source)
            elif isinstance(event_source.type, str):
                groups[event_source.type].append(event_source)

        # Sort
        groups = {k: sorted(v, key=lambda r: r.name, reverse=False) for k, v in groups.items()}

        return {
            "total": total,
            "grouped": groups
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/event-sources/type/{type}",
            tags=["event-source"],
            response_model=dict,
            include_in_schema=server.expose_gui_api)
async def get_event_source_types(type: TypeEnum) -> dict:
    """
    Returns a list of event source types. Each event source requires a source type to define what kind of data is
    that source holding.

    * Endpoint /resources/type/name will return only names and id.
    * Endpoint /resources/type/configuration will return all data.
    """

    try:
        types = event_source_types()

        if type.value == 'name':
            types = {id: t['name'] for id, t in types.items()}

        return {
            "total": len(types),
            "result": types
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/event-source/{id}", tags=["event-source"],
            response_model=EventSource,
            include_in_schema=server.expose_gui_api)
async def load_event_source(id: str):
    try:
        return await storage.driver.event_source.load(id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/event-source", tags=["event-source"],
             include_in_schema=server.expose_gui_api)
async def save_event_source(event_source: EventSource):
    try:
        types = event_source_types()
        if event_source.type in types:
            configuration = types[event_source.type]
            if configuration['configurable'] is True:
                url = urljoin(event_source.url, '/')

                if len(url) > 0 and url[-1] == '/':
                    url = url[:-1]
                client = MicroserviceApi(url,
                                         credentials=Credentials(username=event_source.username,
                                                                 password=event_source.password))
                path = urlparse(event_source.url).path
                if len(path) > 0 and path[-1] != '/':
                    path = path + "/"
                endpoint = f"{path}{event_source.id}"
                try:
                    response = await client.call(endpoint, method="get", data=None)
                    print(response)
                    if response.status == 200:
                        result = await storage.driver.event_source.save(event_source)
                        if result.is_nothing_saved():
                            raise ValueError("Could not save event source.")

                        content = await response.json()
                        content["url"] = url

                        return Response(
                            media_type="application/json",
                            content=json.dumps(content),
                            status_code=status.HTTP_206_PARTIAL_CONTENT
                        )
                    elif response.status == 404:
                        raise ConnectionError("Could not find endpoint {} at {}".format(endpoint, url))

                    elif response.status == 422:

                        return Response(
                            media_type="application/json",
                            content=json.dumps(await response.json()),
                            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
                        )

                    else:
                        raise ConnectionError("Client returned {} status".format(response.status))

                except InvalidURL as e:
                    raise ConnectionError("Could not find endpoint {} at {}".format(endpoint, url))
                except ClientError as e:
                    raise ConnectionError("Client error {}".format(repr(e)))
            else:
                result = await storage.driver.event_source.save(event_source)
                if result.is_nothing_saved():
                    raise ValueError("Could not save event source.")

        return True

    except Exception as e:
        raise HTTPException(status_code=500, detail=repr(e))


@router.delete("/event-source/{id}", tags=["event-source"],
               include_in_schema=server.expose_gui_api)
async def delete_event_source(id: str):
    try:
        result = await storage.driver.event_source.delete(id)
        if result is None:
            return False
        return True
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/event-sources/refresh",
            tags=["event-source"],
            include_in_schema=server.expose_gui_api)
async def refresh_event_sources():
    return await storage.driver.event_source.refresh()


@router.get("/event-sources/entity",
            tags=["event-source"],
            include_in_schema=server.expose_gui_api)
async def list_event_sources_names_and_ids():
    """
    Returns list of event sources. This list contains only id and name.
    """

    try:
        result, total = await storage.driver.event_source.load_all()
        result = [NamedEntity(**r.dict()) for r in result]

        return {
            "total": total,
            "result": list(result)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
