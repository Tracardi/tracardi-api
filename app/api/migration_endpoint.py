import logging
from collections import defaultdict
from fastapi import APIRouter, Depends, HTTPException
from tracardi.context import get_context

from tracardi.domain.version import Version
from tracardi.exceptions.log_handler import log_handler
from tracardi.service.logger_manager import save_logs
from tracardi.service.storage.driver.elastic import raw as raw_db
from tracardi.service.storage.indices_manager import check_indices_mappings_consistency
from app.api.auth.permissions import Permissions
from tracardi.domain.migration_payload import MigrationPayload
from tracardi.process_engine.migration.migration_manager import MigrationManager, MigrationNotFoundException
from tracardi.service.url_constructor import construct_elastic_url
from tracardi.config import elastic, tracardi

router = APIRouter(
    dependencies=[Depends(Permissions(roles=["admin", "developer", "maintainer"]))]
)


logger = logging.getLogger(__name__)
logger.setLevel(tracardi.logging_level)
logger.addHandler(log_handler)


# todo can not find usages
@router.get("/migration/check/from/{version}", tags=["migration"], include_in_schema=tracardi.expose_gui_api)
async def check_migration_consistency(version: str):

    """
    Compares the mappings and indices of the local settings to those in a database, and lists any errors found.
    It also compares the number of records between the current version of tracardi and a previous version (see: prefix),
    and if there are any discrepancies, it checks if they are acceptable differences. If they are, it logs the
    difference as an "INFO", otherwise it logs it as a "WARNING". It then returns a dictionary
    containing the errors found in both the mappings and the indices.
    """

    # If there are differences in local mapping settings and database mappings then this
    # function will list all the errors
    mapping_errors = await check_indices_mappings_consistency()

    # list of acceptable differences
    acceptable_differences = {
        'api-instance': "There maybe more or less api instances in new installation",
        'action': 'The reason could be that new version adds some data like in a case of plugins that are added with every new version.',
        'task': "Current version has some tasks already registered, for example tasks for the import",
        'bridge': "Current version may have more bridges installed",
        'user': "There is at least one more user in the current version that was created during installation. Please review you user list. "
    }

    # Find differences in index counts between versions
    current_version = {index: count async for index, count in raw_db.count_all_indices_by_alias()}
    prev_version = {index: count async for index, count in raw_db.count_all_indices_by_alias()}

    count_errors = defaultdict(list)
    for index, count in current_version.items():
        if index not in prev_version:
            count_errors[index].append(f"Can't find index {index} in previous version")

        if prev_version[index] != current_version[index]:
            if index in acceptable_differences:
                type = "INFO"

                reason = acceptable_differences[index]
            else:
                type = "WARNING"
                reason = "The maybe some slight differences in indices that collect data."

            count_errors[index].append({
                "message": f"The number of records in current {index} is not equal to previous version count. "
                           f"Expected: {prev_version[index]} records to be migrated found "
                           f"{current_version[index]} in current version",
                "type": type,
                "reason": reason

            }
            )

    return {
        "counts": count_errors,
        "mappings": mapping_errors
    }


@router.post("/migration", tags=["migration"], include_in_schema=tracardi.expose_gui_api)
async def run_migration(migration: MigrationPayload):
    try:

        tenant = get_context().tenant

        # For none tenant based migration calculate the tenant name.
        if migration.from_tenant_name is None:
            migration.from_tenant_name = Version._generate_name(migration.from_version)

        manager = MigrationManager(
            from_version=migration.from_version,
            from_prefix=migration.from_tenant_name,
            to_version=MigrationManager.get_current_db_version_prefix(tracardi.version),  # Version as 081
            to_prefix=tenant
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

    finally:
        await save_logs()


@router.get("/migration/{from_db_version}", tags=["migration"], include_in_schema=tracardi.expose_gui_api)
async def get_migration_schemas(from_db_version: str, from_tenant_name: str = None):

    if from_tenant_name is None:
        from_tenant_name = Version._generate_name(from_db_version)

    tenant = get_context().tenant
    try:
        manager = MigrationManager(
            from_version=from_db_version,  # Version as 080
            from_prefix=from_tenant_name,
            # My current db version and tenant
            to_version=MigrationManager.get_current_db_version_prefix(tracardi.version),  # Version as 081
            to_prefix=tenant
        )
        return await manager.get_available_schemas()

    except MigrationNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))

    finally:
        await save_logs()


@router.get("/migrations", tags=["migration"], include_in_schema=tracardi.expose_gui_api, response_model=list)
async def get_migrations_for_current_version():
    return MigrationManager.get_available_migrations_for_version(tracardi.version)
