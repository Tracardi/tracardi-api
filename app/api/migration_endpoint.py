from collections import defaultdict

from fastapi import APIRouter, Depends, HTTPException

from tracardi.service.storage.driver import storage
from tracardi.service.storage.indices_manager import check_indices_mappings_consistency

from app.api.auth.permissions import Permissions
from app.config import server
from tracardi.domain.migration_payload import MigrationPayload
from tracardi.process_engine.migration.migration_manager import MigrationManager, MigrationNotFoundException
from typing import Optional
from tracardi.service.url_constructor import construct_elastic_url
from tracardi.config import elastic, tracardi

router = APIRouter(
    dependencies=[Depends(Permissions(roles=["admin", "developer", "maintainer"]))]
)


@router.get("/migration/check/from/{version}", tags=["migration"])
async def check_migration_consistency(prefix: str):
    # If there are differences in local mapping settings and database mappings then this
    # function will list all the errors
    mapping_errors = await check_indices_mappings_consistency()

    acceptable_differences = {
        'api-instance': "There maybe more or less api instances in new installation",
        'action': 'The reason could be that new version adds some data like in a case of plugins that are added with every new version.',
        'task': "Current version has some tasks already registered, for example tasks for the import",
        'bridge': "Current version may have more bridges installed",
        'user': "There is at least one more user in the current version that was created during installation. Please review you user list. "
    }

    current_version = {index: count async for index, count in storage.driver.raw.count_all_indices_by_alias()}
    prev_version = {index: count async for index, count in storage.driver.raw.count_all_indices_by_alias(prefix)}

    errors = defaultdict(list)
    for index, count in current_version.items():
        if index not in prev_version:
            errors[index].append(f"Can't find index {index} in previous version")

        if prev_version[index] != current_version[index]:
            if index in acceptable_differences:
                type = "INFO"

                reason = acceptable_differences[index]
            else:
                type = "WARNING"
                reason = "The maybe some slight differences in indices that collect data."

            errors[index].append({
                "message": f"The number of records in current {index} is not equal to previous version count. "
                           f"Expected: {prev_version[index]} records to be migrated found "
                           f"{current_version[index]} in current version",
                "type": type,
                "reason": reason

            }
            )

    return errors


@router.post("/migration", tags=["migration"], include_in_schema=server.expose_gui_api)
async def run_migration(migration: MigrationPayload):
    try:
        manager = MigrationManager(
            from_version=migration.from_version,
            to_version=tracardi.version.version,
            from_prefix=migration.from_prefix,
            to_prefix=tracardi.version.name
        )
        elastic_host = construct_elastic_url(
            host=elastic.host if isinstance(elastic.host, str) else elastic.host[0],
            scheme=elastic.scheme,
            username=elastic.http_auth_username,
            password=elastic.http_auth_password
        )
        return await manager.start_migration(
            ids=migration.ids,
            elastic_host=elastic_host
        )

    except MigrationNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/migration/{from_version}", tags=["migration"], include_in_schema=server.expose_gui_api)
async def get_migration_schemas(from_version: str, from_prefix: Optional[str] = None):
    try:
        manager = MigrationManager(
            from_version=from_version,
            to_version=tracardi.version.version,
            from_prefix=from_prefix,
            to_prefix=tracardi.version.name
        )
        return await manager.get_customized_schemas()

    except MigrationNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/migrations", tags=["migration"], include_in_schema=server.expose_gui_api, response_model=list)
async def get_migrations_for_current_version():
    return MigrationManager.get_available_migrations_for_version(tracardi.version)
