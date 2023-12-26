from fastapi import APIRouter, Depends, HTTPException

from app.api.auth.permissions import Permissions
from tracardi.config import tracardi
from tracardi.service.storage.driver.elastic import raw as raw_db
from tracardi.service.storage.elastic_client import ElasticClient
from tracardi.service.storage.index import Resource
from tracardi.service.storage.indices_manager import check_indices_mappings_consistency
from tracardi.service.storage.mapping import get_mappings_by_field_type

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
    return await check_indices_mappings_consistency()


@router.get("/storage/mapping/{index}/metadata", tags=["storage"], include_in_schema=tracardi.expose_gui_api,
            response_model=dict)
async def get_index_mapping_metadata(index: str, filter: str = None):
    """
    Returns metadata of given index (str)
    """

    # if tracardi.multi_tenant:
    #     raise HTTPException(status_code=405, detail="This operation is not allowed for multi-tenant server.")

    result = await raw_db.get_mapping_fields(index)
    if filter is not None:
        result = [item for item in result if item.startswith(filter) and item != filter]
    return {"result": result, "total": len(result)}


@router.get("/storage/mapping/{index}/metadata/type/{field_types}", tags=["storage"], include_in_schema=tracardi.expose_gui_api,
            response_model=dict)
async def get_index_mapping_metadata(index: str, field_types: str):
    """
    Returns fields with given field types of given index (str)
    """

    resource = Resource()
    index = resource[index]
    field_types = field_types.split(',')
    fields = await get_mappings_by_field_type(index.get_write_index(), field_types)

    return {"result": fields, "total": len(fields)}


@router.get("/storage/mapping/{index}", tags=["storage"], include_in_schema=tracardi.expose_gui_api,
            response_model=list)
async def get_index_mapping(index: str):
    """
    Returns mapping of given index (str)
    """

    if tracardi.multi_tenant:
        raise HTTPException(status_code=405, detail="This operation is not allowed for multi-tenant server.")

    mapping = await raw_db.get_mapping(index)
    return mapping.get_field_names()


@router.get("/storage/task/{task_id}", tags=["storage"], include_in_schema=tracardi.expose_gui_api)
async def storage_task_status(task_id: str):
    """
    Returns the status of storage task.
    """

    return await raw_db.task_status(task_id)


@router.get("/storage/reindex/{source}/{destination}", tags=["storage"], include_in_schema=tracardi.expose_gui_api)
async def reindex_data(source: str, destination: str, wait_for_completion: bool = True):
    """
    Copies data from one index to another.
    """

    if tracardi.multi_tenant:
        raise HTTPException(status_code=405, detail="This operation is not allowed for multi-tenant server.")

    return await raw_db.reindex(source, destination, wait_for_completion)


@router.delete("/storage/index/{index_name}", tags=["storage"], include_in_schema=tracardi.expose_gui_api)
async def delete_index(index_name: str):
    """
    Deletes storage index
    """

    if tracardi.multi_tenant:
        raise HTTPException(status_code=405, detail="This operation is not allowed for multi-tenant server.")

    es = ElasticClient.instance()
    return await es.remove_index(index_name)
