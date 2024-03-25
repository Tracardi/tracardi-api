from typing import Optional

from fastapi import APIRouter, Depends, HTTPException

from app.api.auth.permissions import Permissions
from tracardi.config import tracardi
from pydantic import BaseModel, field_validator

from tracardi.service.github_client import GitHubClient
from tracardi.service.setup.setup_configuration import GITHUB_CONFIGURATION
from tracardi.service.storage.mysql.mapping.configuration_mapping import map_to_configuration
from tracardi.service.storage.mysql.mapping.workflow_mapping import map_to_workflow_record
from tracardi.service.storage.mysql.service.configuration_service import ConfigurationService
from tracardi.service.storage.mysql.service.workflow_service import WorkflowService

router = APIRouter(
    dependencies=[Depends(Permissions(roles=["admin", "developer"]))]
)


class GitHubCommit(BaseModel):
    file_name: str
    message: Optional[str] = None

    @field_validator("file_name")
    @classmethod
    def field_name_not_empty(cls, value):
        if not value.strip():
            raise ValueError("File name can not be empty")
        return value

@router.post("/github/workflow/{workflow_id}", tags=["github"], include_in_schema=tracardi.expose_gui_api)
async def commit_workflow_to_github(workflow_id: str, commit: GitHubCommit):
    cs = ConfigurationService()
    record = await cs.load_by_id(GITHUB_CONFIGURATION)
    if not record.exists():
        raise HTTPException(status_code=404, detail="Github configuration missing.")

    configuration = record.map_to_object(map_to_configuration)
    client = GitHubClient(
        token=configuration.get_token(),
        repo_name=configuration.get_repo_name(),
        repo_owner=configuration.get_repo_owner()
    )

    wf = WorkflowService()
    workflow_record = await wf.load_by_id(workflow_id)
    if not workflow_record.exists():
        raise HTTPException(status_code=404, detail=f"Could not find workflow id {workflow_id}. Is it saved?")
    workflow = workflow_record.map_to_object(map_to_workflow_record)

    file_payload = workflow.model_dump_json(indent=2)
    return await client.send_file(file_path=commit.file_name, content=file_payload, message=commit.message)

@router.get("/github/list", tags=["github"], include_in_schema=tracardi.expose_gui_api)
async def list_github_files(path: Optional[str] = None):

    if path is None:
        path = '/'

    cs = ConfigurationService()
    record = await cs.load_by_id(GITHUB_CONFIGURATION)
    if not record.exists():
        raise HTTPException(status_code=404, detail="Github configuration missing.")

    configuration = record.map_to_object(map_to_configuration)
    client = GitHubClient(
        token=configuration.get_token(),
        repo_name=configuration.get_repo_name(),
        repo_owner=configuration.get_repo_owner()
    )
    print(client.list_files(path))
    return [item async for item in client.list_files(path)]

@router.get("/github/load", tags=["github"], include_in_schema=tracardi.expose_gui_api)
async def get_github_file(path: str):
    cs = ConfigurationService()
    record = await cs.load_by_id(GITHUB_CONFIGURATION)
    if not record.exists():
        raise HTTPException(status_code=404, detail="Github configuration missing.")

    configuration = record.map_to_object(map_to_configuration)
    client = GitHubClient(
        token=configuration.get_token(),
        repo_name=configuration.get_repo_name(),
        repo_owner=configuration.get_repo_owner()
    )
    return await client.load_file(path)
