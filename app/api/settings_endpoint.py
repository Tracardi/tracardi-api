from typing import List, Optional
from tracardi.config import elastic, redis_config, tracardi, memory_cache
from app.api.auth.authentication import get_current_user
from app.config import *
from fastapi import APIRouter, Depends
from tracardi.domain.settings import SystemSettings

system_settings = [
    SystemSettings(
        **{
            "label": "USER_NAME",
            "value": auth.user,
            "desc": "Tracardi username."
        }
    ),
    SystemSettings(
        **{
            "label": "PASSWORD",
            "value": auth.password,
            "desc": "Tracardi password."
        }
    ),
    SystemSettings(
        **{
            "label": "UPDATE_PLUGINS_ON_STARTUP",
            "value": server.update_plugins_on_start_up,
            "desc": "Update plugins on startup or not."
        }
    ),
    SystemSettings(
        **{
            "label": "DEBUG_MAKE_SLOWER_RESPONSES",
            "value": server.make_slower_responses,
            "desc": "Slow responses by adding a wait time. This is for debug purposes only, defaults to 0."
        }
    ),
    SystemSettings(
        **{
            "label": "RUN_HEARTBEAT_EVERY",
            "value": server.heartbeat_every,
            "desc": "The interval of running heartbeat in seconds, "
                    "defaults to 300."
        }
    ),
    SystemSettings(
        **{
            "label": "TASKS_EVERY",
            "value": server.tasks_every,
            "desc": "The interval of running tasks in seconds, "
                    "defaults to 1."
        }
    ),
    SystemSettings(
        **{
            "label": "AUTOLOAD_PAGE_SIZE",
            "value": server.page_size,
            "desc": "The size of automatically loaded page, defaults"
                    " to 25."
        }
    ),
    SystemSettings(
        **{
            "label": "EXPOSE_GUI_API",
            "value": server.expose_gui_api,
            "desc": "Expose GUI API or not, defaults to True, "
                    "can be changed by setting to 'yes' (then it's True) or 'no', "
                    "which makes it False."
        }
    ),
    SystemSettings(
        **{
            "label": "RESET_PLUGINS",
            "value": server.reset_plugins,
            "desc": "Reset plugins data in ElasticSearch database, defaults to False. "
                    "Plug-ins are recreated with every Tracardi restart."
        }
    ),
    SystemSettings(
        **{
            "label": "TRACK_DEBUG",
            "value": tracardi.track_debug,
            "desc": "Track debug or not, defaults to False."
        }
    ),
    SystemSettings(
        **{
            "label": "CACHE_PROFILE",
            "value": tracardi.cache_profiles,
            "desc": "Cache profiles or not, defaults to False."
        }
    ),
    SystemSettings(
        **{
            "label": "SYNC_PROFILE_TRACKS",
            "value": tracardi.sync_profile_tracks,
            "desc": "No desc"
        }
    ),
    SystemSettings(
        **{
            "label": "STORAGE_DRIVER",
            "value": tracardi.storage_driver,
            "desc": "The name of storage driver, defaults to 'elastic'."
        }
    ),
    SystemSettings(
        **{
            "label": "LOGGING_LEVEL",
            "value": tracardi.logging_level,
            "desc": "The logging level. Defaults to logging.WARNING."
        }
    ),
    SystemSettings(
        **{
            "label": "SOURCE_TTL",
            "value": memory_cache.source_ttl,
            "desc": "No desc, defaults to 60."
        }
    ),
    SystemSettings(
        **{
            "label": "ELASTIC_HOST",
            "value": elastic.host,
            "desc": "Elastic host. Defaults to '127.0.0.1'."
        }
    ),
    SystemSettings(
        **{
            "label": "ELASTIC_SNIFF_ON_START",
            "value": elastic.sniff_on_start,
            "desc": "Defaults to None."
        }
    ),
    SystemSettings(
        **{
            "label": "ELASTIC_SNIFF_ON_CONNECTION_FAIL",
            "value": elastic.sniff_on_connection_fail,
            "desc": "Defaults to None."
        }
    ),
    SystemSettings(
        **{
            "label": "ELASTIC_SNIFFER_TIMEOUT",
            "value": elastic.sniffer_timeout,
            "desc": "Defaults to None."
        }
    ),
    SystemSettings(
        **{
            "label": "ELASTIC_HTTP_AUTH_USERNAME",
            "value": elastic.http_auth_username,
            "desc": "Defaults to None."
        }
    ),
    SystemSettings(
        **{
            "label": "ELASTIC_HTTP_AUTH_PASSWORD",
            "value": elastic.http_auth_password,
            "desc": "Defaults to None."
        }
    ),
    SystemSettings(
        **{
            "label": "ELASTIC_SCHEME",
            "value": elastic.scheme,
            "desc": "Defaults to None."
        }
    ),
    SystemSettings(
        **{
            "label": "ELASTIC_CAFILE",
            "value": elastic.cafile,
            "desc": "Defaults to None."
        }
    ),
    SystemSettings(
        **{
            "label": "ELASTIC_API_KEY",
            "value": elastic.api_key,
            "desc": "Defaults to None."
        }
    ),
    SystemSettings(
        **{
            "label": "ELASTIC_CLOUD_ID",
            "value": elastic.cloud_id,
            "desc": "Defaults to None."
        }
    ),
    SystemSettings(
        **{
            "label": "ELASTIC_MAX_CONN",
            "value": elastic.maxsize,
            "desc": "Defaults to None."
        }
    ),
    SystemSettings(
        **{
            "label": "ELASTIC_HTTP_COMPRESS",
            "value": elastic.http_compress,
            "desc": "Defaults to None."
        }
    ),
    SystemSettings(
        **{
            "label": "ELASTIC_VERIFY_CERTS",
            "value": elastic.verify_certs,
            "desc": "Defaults to None. Can be changed by being set to 'yes'."
        }
    ),
    SystemSettings(
        **{
            "label": "ELASTIC_SQL_TRANSLATE_URL",
            "value": elastic.sql_translate_url,
            "desc": "Defaults to '/_sql/translate'."
        }
    ),
    SystemSettings(
        **{
            "label": "ELASTIC_SQL_TRANSLATE_METHOD",
            "value": elastic.sql_translate_method,
            "desc": "Defaults to 'POST'."
        }
    ),
    SystemSettings(
        **{
            "label": "ELASTIC_REFRESH_PROFILES_AFTER_SAVE",
            "value": elastic.refresh_profiles_after_save,
            "desc": "Defaults to False."
        }
    ),
    SystemSettings(
        **{
            "label": "ELASTIC_LOGGING_LEVEL",
            "value": elastic.logging_level,
            "desc": "Defaults to logging.WARNING."
        }
    ),
    SystemSettings(
        **{
            "label": "REDIS_HOST",
            "value": redis_config.redis_host,
            "desc": "Defaults to 'redis://localhost:6379'."
        }
    ),
]

router = APIRouter(
    dependencies=[Depends(get_current_user)]
)


@router.get("/setting/{name}", tags=["settings"],
            include_in_schema=server.expose_gui_api,
            response_model=Optional[SystemSettings])
async def get_system_settings(name: str) -> Optional[SystemSettings]:
    for setting in system_settings:
        if setting.label == name:
            return setting
    return None


@router.get("/settings", tags=["settings"],
            include_in_schema=server.expose_gui_api,
            response_model=List[SystemSettings])
async def get_system_settings() -> List[SystemSettings]:
    return system_settings
