from datetime import datetime

from fastapi import APIRouter

from tracardi.domain.api_instance import ApiInstance
from tracardi.service.license import License

from tracardi.config import tracardi

router = APIRouter()


@router.get("/info/version", tags=["info"], include_in_schema=tracardi.expose_gui_api, response_model=str)
async def get_version():
    """
    Returns info about Tracardi API version
    """
    return tracardi.version.version


@router.get("/info/version/details", tags=["info"])
async def get_current_backend_version():

    """
    Returns current backend version with previous versions.
    """

    version = tracardi.version.model_dump(mode='json')
    version['instance'] = ApiInstance().id

    if License.has_license():
        license = License.check()
        version['owner'] = license.owner
        version['expires'] = datetime.fromtimestamp(license.expires)
        version['licenses'] = list(license.get_service_ids())
    else:
        version['owner'] = "Tracardi"
        version['expires'] = "Never"
        version['licenses'] = ["MIT + Common Clause"]
    return version
