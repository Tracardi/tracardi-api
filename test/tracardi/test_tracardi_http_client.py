from tracardi.service.tracardi_http_client import HttpClient
from ..utils import Endpoint
import asyncio


async def _should_get():
    async with HttpClient(5, 200, headers={"some-header": "1"}) as client:
        async with client.get(Endpoint.host("/healthcheck"), json={}) as response:

            assert response.status == 200
            response = await response.json()
            assert "headers" in response
            assert response["headers"]["some-header"] == "1"


async def _should_post():
    async with HttpClient(5, 200, headers={"some-header": "1"}) as client:
        async with client.post(Endpoint.host("/healthcheck"), json={}) as response:

            assert response.status == 200
            response = await response.json()
            assert "headers" in response
            assert response["headers"]["some-header"] == "1"


async def _should_put():
    async with HttpClient(5, 200, headers={"some-header": "1"}) as client:
        async with client.put(Endpoint.host("/healthcheck"), json={}) as response:

            assert response.status == 200
            response = await response.json()
            assert "headers" in response
            assert response["headers"]["some-header"] == "1"


async def _should_delete():
    async with HttpClient(5, 200, headers={"some-header": "1"}) as client:
        async with client.delete(Endpoint.host("/healthcheck"), json={}) as response:

            assert response.status == 200
            response = await response.json()
            assert "headers" in response
            assert response["headers"]["some-header"] == "1"


async def _should_give_404():
    async with HttpClient(5, 200, headers={"some-header": "1"}) as client:
        async with client.get(Endpoint.host("/this-endpoint-does-not-exist"), json={}) as response:

            # Unclosed connection warning is likely to some error in aiohttp, which is about to be fixed in 4.0.0
            # Notice that it happens only with Tracardi API (try https://google.com/awkjdbakjwhdajhwdjhabwd)
            # For confirming retry behavior - check logs. This test should result in 404 log 5 times.

            assert response.status == 404


def test_tracardi_http_client():
    asyncio.get_event_loop().run_until_complete(_should_get())
    asyncio.get_event_loop().run_until_complete(_should_post())
    asyncio.get_event_loop().run_until_complete(_should_put())
    asyncio.get_event_loop().run_until_complete(_should_delete())
    asyncio.get_event_loop().run_until_complete(_should_give_404())

