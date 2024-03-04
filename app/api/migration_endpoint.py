import os

import alembic.config
from alembic.config import Config
from alembic.script import ScriptDirectory
from alembic.runtime.environment import EnvironmentContext
from sqlalchemy import create_engine

from collections import defaultdict
from fastapi import APIRouter, Depends, HTTPException

from app.api.auth.permissions import Permissions
from tracardi.context import get_context
from tracardi.domain.version import Version
from tracardi.exceptions.log_handler import get_logger
from tracardi.service.logger_manager import save_logs
from tracardi.service.storage.driver.elastic import raw as raw_db
from tracardi.service.storage.indices_manager import check_indices_mappings_consistency
from tracardi.domain.migration_payload import MigrationPayload
from tracardi.process_engine.migration.migration_manager import MigrationManager, MigrationNotFoundException
from tracardi.service.url_constructor import construct_elastic_url
from tracardi.config import elastic, tracardi, mysql

def get_pending_migrations(alembic_cfg_path, sqlalchemy_url):
    # Load Alembic configuration and set the SQLALCHEMY database URL
    alembic_cfg = Config(alembic_cfg_path)
    alembic_cfg.set_main_option('sqlalchemy.url', sqlalchemy_url)

    # Create an engine and bind it to the Alembic configuration
    engine = create_engine(sqlalchemy_url)
    alembic_cfg.attributes['connection'] = engine.connect()

    # Get script directory from configuration
    script = ScriptDirectory.from_config(alembic_cfg)

    # List to hold pending migrations
    pending_migrations = []

    # Use EnvironmentContext to get the current revision and heads
    with EnvironmentContext(
            alembic_cfg,
            script,
            fn=lambda rev, context: pending_migrations.extend(
                script.iterate_revisions(rev, "heads"))
    ):
        # Get current revision
        current_revision = script.get_current_revision()

    # Cleanup
    alembic_cfg.attributes['connection'].close()

    # Filter migrations, starting from the current revision to the head
    return [rev.cmd_format(False) for rev in pending_migrations if rev.revision > current_revision]



router = APIRouter(
    dependencies=[Depends(Permissions(roles=["admin", "maintainer"]))]
)


logger = get_logger(__name__)
_local_path = os.path.dirname(__file__)

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


@router.post("/migration/elasticsearch", tags=["migration"], include_in_schema=tracardi.expose_gui_api)
async def run_elasticsearch_migration(migration: MigrationPayload):
    try:

        context = get_context()

        tenant = context.tenant

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
            elastic_host=elastic_host,
            context=context
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


@router.post("/migration/mysql/upgrade", tags=["migration"], include_in_schema=tracardi.expose_gui_api)
def run_mysql_migration_script(generate_revision: bool = False):
    os.chdir(os.path.realpath(f"{_local_path}/.."))

    if generate_revision:
        try:
            alembicArgs = ['revision', '--autogenerate', '-m', 'Create migrations form API']
            alembic.config.main(argv=alembicArgs)
        except Exception as e:
            return str(e)

    alembicArgs = ['--raiseerr', 'upgrade', 'head' ]
    alembic.config.main(argv=alembicArgs)


# Example usage
# alembic_cfg_path = '../alembic.ini'
#
# sqlalchemy_url = f"{mysql.uri(async_driver=False)}/{mysql.mysql_database}"
# print(sqlalchemy_url)
# pending_migrations = get_pending_migrations(alembic_cfg_path, sqlalchemy_url)
# print("Pending Migrations:")
# for migration in pending_migrations:
#     print(migration)