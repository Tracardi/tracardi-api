from fastapi import APIRouter
from fastapi import HTTPException, Depends
from tracardi.service.storage.factory import StorageFor, StorageForBulk

from .auth.authentication import get_current_user
from tracardi.domain.project import Project
from tracardi.domain.entity import Entity
from tracardi.domain.value_object.bulk_insert_result import BulkInsertResult
from ..config import server

router = APIRouter(
    dependencies=[Depends(get_current_user)]
)


@router.get("/projects", tags=["project"], include_in_schema=server.expose_gui_api)
async def get_projects(query: str = None):
    """
    Returns list of existing projects
    """
    try:
        result = await StorageForBulk().index('project').load()
        return list(result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/project/{id}", tags=["project"], response_model=Project, include_in_schema=server.expose_gui_api)
async def get_project_by_id(id: str):
    """
    Returns project with given ID (str)
    """
    try:
        project = Entity(id=id)
        return await StorageFor(project).index('project').load()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/project", tags=["project"], response_model=BulkInsertResult, include_in_schema=server.expose_gui_api)
async def add_project(project: Project):
    """
    Creates new project in database
    """
    try:
        return await StorageFor(project).index().save()
        # return await project.storage().save()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/project/{id}", tags=["project"], response_model=dict, include_in_schema=server.expose_gui_api)
async def delete_project(id: str):
    """
    Deletes project with given ID (str)
    """
    try:
        project = Entity(id=id)
        return await StorageFor(project).index('project').delete()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
