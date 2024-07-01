from fastapi import APIRouter
from tracardi.service.tracardi_http_client import HttpClient

router = APIRouter()


@router.get("/feed", tags=["info"])
async def get_rss():
    """
    Returns info about Tracardi Installed Versions
    """

    async with HttpClient(3, [200], headers={"Content-Type": "application/rss+xml; charset=UTF-8"}) as client:
        async with client.get(
                url=f"https://www.tracardi.com/index.php/feed",
        ) as response:
            return await response.read()
