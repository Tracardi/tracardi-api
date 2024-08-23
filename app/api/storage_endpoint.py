from fastapi import APIRouter, Depends, HTTPException

from app.api.auth.permissions import Permissions
from tracardi.config import tracardi
from tracardi.service.storage.elastic.interface.gui.storage import get_indices_mappings_consistency, \
    load_index_mapping_metadata, remove_index
from tracardi.service.storage.elastic.interface.gui.mapping import load_mappings_by_field_type, load_index_field_names,\
    load_task_status
from tracardi.service.storage.index import Resource

router = APIRouter(
    dependencies=[Depends(Permissions(roles=["admin", "maintainer"]))]
)


@router.get("/storage/mapping/check", tags=["storage"], include_in_schema=tracardi.expose_gui_api,
            response_model=dict)
async def check_indices_mapping_consistency():
    """
    Checks indices mapping consistency. Returns errors if any.
    This code is checking the mapping of an Elasticsearch
    index against a system mapping file. It loops through
    a dictionary of resources and for each resource, it
    retrieves the system mapping file and loads it into memory.
    It then compares this system mapping to the mapping of an
    Elasticsearch index that is being written to. If there are
    any differences between the two mappings, it saves these
    differences in a dictionary. And, it returns the result dictionary at the end.
    """
    return await get_indices_mappings_consistency()


@router.get("/storage/mapping/{index}/metadata", tags=["storage"], include_in_schema=tracardi.expose_gui_api,
            response_model=dict)
async def return_index_mapping_metadata(index: str, filter: str = None):
    """
    Returns metadata of given index (str)
    """

    if tracardi.multi_tenant:
        raise HTTPException(status_code=405, detail="This operation is not allowed for multi-tenant server.")

    return load_index_mapping_metadata(index, filter)


@router.get("/storage/mapping/{index}/metadata/type/{field_types}", tags=["storage"], include_in_schema=tracardi.expose_gui_api,
            response_model=dict)
async def get_index_mapping_metadata(index: str, field_types: str):
    """
    Returns fields with given field types of given index (str)
    """

    resource = Resource()
    index = resource[index]
    field_types = field_types.split(',')
    fields = await load_mappings_by_field_type(index.get_write_index(), field_types)

    return {"result": fields, "total": len(fields)}


@router.get("/storage/mapping/{index}", tags=["storage"], include_in_schema=tracardi.expose_gui_api,
            response_model=list)
async def get_index_mapping(index: str):

    # TODO check if this is used

    """
    Returns mapping of given index (str)
    """

    if tracardi.multi_tenant:
        raise HTTPException(status_code=405, detail="This operation is not allowed for multi-tenant server.")

    return load_index_field_names(index)


@router.get("/storage/task/{task_id}", tags=["storage"], include_in_schema=tracardi.expose_gui_api)
async def storage_task_status(task_id: str):
    """
    Returns the status of storage task.
    """

    return await load_task_status(task_id)


@router.delete("/storage/index/{index_name}", tags=["storage"], include_in_schema=tracardi.expose_gui_api)
async def delete_index(index_name: str):
    """
    Deletes storage index
    """

    if tracardi.multi_tenant:
        raise HTTPException(status_code=405, detail="This operation is not allowed for multi-tenant server.")

    return await remove_index(index_name)
