from typing import List, Any
from app.config import *
from fastapi import APIRouter
from pydantic import BaseModel
from tracardi.config import *


class EnvVar(BaseModel):
    suffix: str
    label: str
    value: Any
    desc: str

    def generate_endpoint(self):
        return "/settings/{}".format(self.suffix)


def get_envs() -> List[EnvVar]:
    return [
        EnvVar(
            **{
                "label": "USER_NAME",
                "suffix": "user",
                "value": auth.user,
                "desc": "Environmental variable containing username."
            }
        ),
        EnvVar(
            **{
                "label": "PASSWORD",
                "suffix": "password",
                "value": auth.password,
                "desc": "Environmental variable containing password."
            }
        ),
        EnvVar(
            **{
                "label": "UPDATE_PLUGINS_ON_STARTUP",
                "suffix": "update_plugins_on_startup",
                "value": server.update_plugins_on_start_up,
                "desc": "Environmental variable telling TracardiAPI to update plugins on startup or not."
            }
        ),
        EnvVar(
            **{
                "label": "DEBUG_MAKE_SLOWER_RESPONSES",
                "suffix": "make_slower_responses",
                "value": server.make_slower_responses,
                "desc": "Environmental variable telling TracardiAPI the speed of debug responses, defaults to 0."
            }
        ),
        EnvVar(
            **{
                "label": "RUN_HEARTBEAT_EVERY",
                "suffix": "heartbeat_every",
                "value": server.heartbeat_every,
                "desc": "Environmental variable telling TracardiAPI the interval of running heartbeat in seconds, "
                        "defaults to 300."
            }
        ),
        EnvVar(
            **{
                "label": "TASKS_EVERY",
                "suffix": "tasks_every",
                "value": server.tasks_every,
                "desc": "Environmental variable telling TracardiAPI the interval of running tasks in seconds, "
                        "defaults to 1."
            }
        ),
        EnvVar(
            **{
                "label": "AUTOLOAD_PAGE_SIZE",
                "suffix": "page_size",
                "value": server.page_size,
                "desc": "Environmental variable telling TracardiAPI the size of automatically loaded page, defaults"
                        " to 25."
            }
        ),
        EnvVar(
            **{
                "label": "EXPOSE_GUI_API",
                "suffix": "expose_gui_api",
                "value": server.expose_gui_api,
                "desc": "Environmental variable telling TracardiAPI to expose GUI API or not, defaults to True, "
                        "can be changed by setting this variable to 'yes' (then it's True) or something else, "
                        "which makes it False."
            }
        ),
        EnvVar(
            **{
                "label": "RESET_PLUGINS",
                "suffix": "reset_plugins",
                "value": server.reset_plugins,
                "desc": "Environmental variable telling TracardiAPI to reset plugins data in ElasticSearch database"
                        " or not to do so, defaults to False, can be changed as previous one."
            }
        ),
        EnvVar(
            **{
                "label": "TRACK_DEBUG",
                "suffix": "track_debug",
                "value": tracardi.track_debug,
                "desc": "Environmental variable telling Tracardi to track debug or not, defaults to False."
            }
        ),
        EnvVar(
            **{
                "label": "CACHE_PROFILE",
                "suffix": "cache_profiles",
                "value": tracardi.cache_profiles,
                "desc": "Environmental variable telling Tracardi to cache profiles or not, defaults to False."
            }
        ),
        EnvVar(
            **{
                "label": "SYNC_PROFILE_TRACKS",
                "suffix": "sync_profile_tracks",
                "value": tracardi.sync_profile_tracks,
                "desc": "No desc"
            }
        ),
        EnvVar(
            **{
                "label": "STORAGE_DRIVER",
                "suffix": "storage_driver",
                "value": tracardi.storage_driver,
                "desc": "Environmental variable telling Tracardi the name of storage driver, defaults to 'elastic'."
            }
        ),
        EnvVar(
            **{
                "label": "LOGGING_LEVEL",
                "suffix": "logging_level",
                "value": tracardi.logging_level,
                "desc": "Environmental variable telling Tracardi the logging level. Defaults to logging.WARNING."
            }
        ),
        EnvVar(
            **{
                "label": "SOURCE_TTL",
                "suffix": "source_ttl",
                "value": memory_cache.source_ttl,
                "desc": "No desc, defaults to 60."
            }
        ),
        EnvVar(
            **{
                "label": "ELASTIC_HOST",
                "suffix": "host",
                "value": elastic.host,
                "desc": "Environmental variable telling Tracardi the name of elastic host. Defaults to '127.0.0.1'."
            }
        ),
        EnvVar(
            **{
                "label": "ELASTIC_SNIFF_ON_START",
                "suffix": "sniff_on_start",
                "value": elastic.sniff_on_start,
                "desc": "Defaults to None."
            }
        ),
        EnvVar(
            **{
                "label": "ELASTIC_SNIFF_ON_CONNECTION_FAIL",
                "suffix": "sniff_on_connection_fail",
                "value": elastic.sniff_on_connection_fail,
                "desc": "Defaults to None."
            }
        ),
        EnvVar(
            **{
                "label": "ELASTIC_SNIFFER_TIMEOUT",
                "suffix": "sniffer_timeout",
                "value": elastic.sniffer_timeout,
                "desc": "Defaults to None."
            }
        ),
        EnvVar(
            **{
                "label": "ELASTIC_HTTP_AUTH_USERNAME",
                "suffix": "http_auth_username",
                "value": elastic.http_auth_username,
                "desc": "Defaults to None."
            }
        ),
        EnvVar(
            **{
                "label": "ELASTIC_HTTP_AUTH_PASSWORD",
                "suffix": "http_auth_password",
                "value": elastic.http_auth_password,
                "desc": "Defaults to None."
            }
        ),
        EnvVar(
            **{
                "label": "ELASTIC_SCHEME",
                "suffix": "scheme",
                "value": elastic.scheme,
                "desc": "Defaults to None."
            }
        ),
        EnvVar(
            **{
                "label": "ELASTIC_CAFILE",
                "suffix": "cafile",
                "value": elastic.cafile,
                "desc": "Defaults to None."
            }
        ),
        EnvVar(
            **{
                "label": "ELASTIC_API_KEY",
                "suffix": "api_key",
                "value": elastic.api_key,
                "desc": "Defaults to None."
            }
        ),
        EnvVar(
            **{
                "label": "ELASTIC_CLOUD_ID",
                "suffix": "cloud_id",
                "value": elastic.cloud_id,
                "desc": "Defaults to None."
            }
        ),
        EnvVar(
            **{
                "label": "ELASTIC_MAX_CONN",
                "suffix": "maxsize",
                "value": elastic.maxsize,
                "desc": "Defaults to None."
            }
        ),
        EnvVar(
            **{
                "label": "ELASTIC_HTTP_COMPRESS",
                "suffix": "http_compress",
                "value": elastic.http_compress,
                "desc": "Defaults to None."
            }
        ),
        EnvVar(
            **{
                "label": "ELASTIC_VERIFY_CERTS",
                "suffix": "verify_certs",
                "value": elastic.verify_certs,
                "desc": "Defaults to None. Can be changed by being set to 'yes'."
            }
        ),
        EnvVar(
            **{
                "label": "ELASTIC_SQL_TRANSLATE_URL",
                "suffix": "sql_translate_url",
                "value": elastic.sql_translate_url,
                "desc": "Defaults to '/_sql/translate'."
            }
        ),
        EnvVar(
            **{
                "label": "ELASTIC_SQL_TRANSLATE_METHOD",
                "suffix": "sql_translate_method",
                "value": elastic.sql_translate_method,
                "desc": "Defaults to 'POST'."
            }
        ),
        EnvVar(
            **{
                "label": "ELASTIC_REFRESH_PROFILES_AFTER_SAVE",
                "suffix": "refresh_profiles_after_save",
                "value": elastic.refresh_profiles_after_save,
                "desc": "Defaults to False."
            }
        ),
        EnvVar(
            **{
                "label": "ELASTIC_LOGGING_LEVEL",
                "suffix": "elastic_logging_level",
                "value": elastic.logging_level,
                "desc": "Defaults to logging.WARNING."
            }
        ),
        EnvVar(
            **{
                "label": "REDIS_HOST",
                "suffix": "redis_host",
                "value": redis_config.redis_host,
                "desc": "Defaults to 'redis://localhost:6379'."
            }
        ),
    ]


router = APIRouter()
envs = get_envs()


@router.get("/settings", tags=["environmental_variables"], include_in_schema=server.expose_gui_api)
async def get_settings():
    return [
        {
            env.label: env.value,
            "description": env.desc,
            "endpoint": env.generate_endpoint()
        } for env in envs
    ]


@router.get("/settings/{variable_name}", tags=["specified_environmental_variable"],
            include_in_schema=server.expose_gui_api)
async def get_setting(variable_name: str = ""):
    env = [var for var in envs if var.suffix == variable_name][0]
    return {
        env.label: env.value,
        "description": env.desc,
        "endpoint": env.generate_endpoint()
    }
