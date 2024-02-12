from datetime import datetime

from fastapi import APIRouter

from service.grouping import get_grouped_result
from tracardi.domain.api_instance import ApiInstance
from tracardi.domain.installation_status import installation_status
from tracardi.service.license import License

from tracardi.config import tracardi
from tracardi.service.storage.mysql.mapping.version_mapping import map_to_version
from tracardi.service.storage.mysql.service.version_service import VersionService

router = APIRouter()


@router.get("/info/versions", tags=["info"], include_in_schema=tracardi.expose_gui_api)
async def get_versions():
    """
    Returns info about Tracardi Installed Versions
    """

    vs = VersionService()
    records = await vs.load_all(limit=100)
    return get_grouped_result("Versions", records, map_to_version)


@router.get("/info/version", tags=["info"], include_in_schema=tracardi.expose_gui_api, response_model=str)
async def get_version():
    """
    Returns info about Tracardi API version
    """
    return tracardi.version.version


@router.get("/info/version/details", tags=["info"])
@router.get("/")
async def get_current_backend_version():

    """
    Returns current backend version with previous versions.
    """

    version = tracardi.version.model_dump(mode='json')
    version['instance'] = ApiInstance().id
    version['installed'] = await installation_status.get_status()

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
