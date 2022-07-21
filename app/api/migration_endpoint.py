from fastapi import APIRouter, Depends, HTTPException

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

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


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

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/migrations", tags=["migration"], include_in_schema=server.expose_gui_api, response_model=list)
async def get_migrations_for_current_version():
    try:
        return MigrationManager.get_available_migrations_for_version(tracardi.version)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
