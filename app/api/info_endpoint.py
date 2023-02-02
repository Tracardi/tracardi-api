from datetime import datetime

from fastapi import APIRouter
from tracardi.service.license import License

from app.config import server
from tracardi.config import tracardi
from tracardi.domain.version import Version
from tracardi.service.storage.driver import storage

router = APIRouter()


@router.get("/info/version", tags=["info"], include_in_schema=server.expose_gui_api, response_model=str)
async def get_version():
    """
    Returns info about Tracardi API version
    """
    return tracardi.version.version


@router.get("/info/version/details", tags=["info"], include_in_schema=server.expose_gui_api)
async def get_current_backend_version():

    """
    Returns current backend version with previous versions.
    """

    result = await storage.driver.version.load()
    version = dict(result)
    license = License.check()
    version['owner'] = license.owner
    version['expires'] = datetime.fromtimestamp(license.expires)
    version['licenses'] = list(license.get_service_ids())

    return version
