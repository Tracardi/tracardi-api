from typing import List, Optional

from app.api.auth.permissions import Permissions
from tracardi.config import elastic, redis_config, tracardi, memory_cache
from app.config import *
from fastapi import APIRouter, Depends
from tracardi.domain.settings import SystemSettings

system_settings = [
    SystemSettings(
        **{
            "label": "UPDATE_PLUGINS_ON_STARTUP",
            "value": server.update_plugins_on_start_up,
            "desc": "Default: no. If equals yes it will update all installed plugins on Tracardi start."
        }
    ),
    SystemSettings(
        **{
            "label": "DEBUG_MAKE_SLOWER_RESPONSES",
            "value": server.make_slower_responses,
            "desc": "Default: 0. This variable is for testing purposes only. It sets the number of seconds each "
                    "endpoint should be slowed in order to see the GUI responses."
        }
    ),
    SystemSettings(
        **{
            "label": "API_DOCS",
            "value": server.api_docs,
            "desc": "Default: Yes. Turns off APi documentations at /docs."
        }
    ),
    SystemSettings(
        **{
            "label": "RUN_HEARTBEAT_EVERY",
            "value": server.heartbeat_every,
            "desc": "Default: 300. The time each worker reports its health."
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
            "label": "TRACK_DEBUG",
            "value": tracardi.track_debug,
            "desc": "Track debug or not, defaults to False."
        }
    ),
    SystemSettings(
        **{
            "label": "QUERY_LANGUAGE",
            "value": tracardi.query_language,
            "desc": "Defines what type of query language to use for filtering data. Default: Kibana Query Language (kql)."
                    " Other possible values Tracardi Query Language (tql)"
        }
    ),
    SystemSettings(
        **{
            "label": "TRACARDI_PRO_HOST",
            "value": tracardi.tracardi_pro_host,
            "desc": "Defines the Tracardi Pro Services Host."
        }
    ),
    SystemSettings(
        **{
            "label": "TRACARDI_PRO_PORT",
            "value": tracardi.tracardi_pro_port,
            "desc": "Defines the Tracardi Pro Services Port."
        }
    ),
    SystemSettings(
        **{
            "label": "TRACARDI_SCHEDULER_HOST",
            "value": tracardi.tracardi_scheduler_host,
            "desc": "Defines the Tracardi Pro Scheduler Host."
        }
    ),

    SystemSettings(
        **{
            "label": "CACHE_PROFILE",
            "value": tracardi.cache_profiles,
            "desc": "Default: no. Profiles can be cached, but it is not recommended as this option is experimental."
        }
    ),
    SystemSettings(
        **{
            "label": "SYNC_PROFILE_TRACKS",
            "value": tracardi.sync_profile_tracks,
            "desc": "Variable sets Tracardi to synchronize profile tracks or not, defaults to False. By default "
                    "Tracardi runs profile updates in parallel. This may lead to profile changes that are not up to "
                    "date if the changes to profile are very quick. To sync profile changes set this variable "
                    "to 'yes'. This features requires "
                    "REDIS."
        }
    ),
    SystemSettings(
        **{
            "label": "POSTPONE_DESTINATION_SYNC",
            "value": tracardi.postpone_destination_sync,
            "desc": "Postpone destination synchronisation. Default 0, means do not wait. Destinations are called only "
                    "when the profile is changed. If there is a stream of changes then with every change of profile "
                    "synchronisation will be triggered. To avoid unnecessary calls to external systems you can set this "
                    "variable to eg. 60 seconds and Tracardi will wait between 60 and 120 seconds after the last "
                    "change of profile before it will trigger destination synchronisation. This features requires "
                    "REDIS."
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
            "desc": "Default: 60. Each resource read is cached for given seconds. That means that when you change any "
                    "resource data, e.g. credentials it wil be available with max 60 seconds."
        }
    ),
    SystemSettings(
        **{
            "label": "ELASTIC_HOST",
            "value": elastic.host,
            "desc": "Default: 127.0.0.1. This setting defines a IP address of elastic search instance. See Connecting "
                    "to elastic cluster for more information how to connect to a cluster of servers."
        }
    ),
    SystemSettings(
        **{
            "label": "ELASTIC_INDEX_SHARDS",
            "value": elastic.shards,
            "desc": "Default: 5. Number of shards per index."
        }
    ),
    SystemSettings(
        **{
            "label": "ELASTIC_INDEX_REPLICAS",
            "value": elastic.replicas,
            "desc": "Default: 5. Number of replicas of index."
        }
    ),
    SystemSettings(
        **{
            "label": "INSTANCE_PREFIX",
            "value": tracardi.version.name,
            "desc": "Default: None. This setting defines a prefix for all tracardi indices."
        }
    ),
    SystemSettings(
        **{
            "label": "ELASTIC_SNIFF_ON_START",
            "value": elastic.sniff_on_start,
            "desc": "Default: None. When you enable this option, the client will attempt to execute an elasitcsearch "
                    "sniff request during the client initialization or first usage. Search documentation for "
                    "sniffing to get more information."
        }
    ),
    SystemSettings(
        **{
            "label": "ELASTIC_SNIFF_ON_CONNECTION_FAIL",
            "value": elastic.sniff_on_connection_fail,
            "desc": "Default: None. If you enable this option, the client will attempt to execute a sniff request every"
                    " time a node is faulty, which means a broken connection or a dead node."
        }
    ),
    SystemSettings(
        **{
            "label": "ELASTIC_SNIFFER_TIMEOUT",
            "value": elastic.sniffer_timeout,
            "desc": "Default: None, Time out for sniff operation."
        }
    ),
    SystemSettings(
        **{
            "label": "ELASTIC_HTTP_AUTH_USERNAME",
            "value": elastic.http_auth_username,
            "desc": "Default: None. Elastic search username. Search for elastic authentication "
                    "for more information on how to configure connection to elastic."
        }
    ),
    SystemSettings(
        **{
            "label": "ELASTIC_HTTP_AUTH_PASSWORD",
            "value": "Set" if elastic.http_auth_password is not None else "Unset",
            "desc": "Default: None. Elastic search password. Search for elastic authentication "
                    "for more information on how to configure connection to elastic."
        }
    ),
    SystemSettings(
        **{
            "label": "ELASTIC_SCHEME",
            "value": elastic.scheme,
            "desc": "Default: http. Available options http, https."
        }
    ),
    SystemSettings(
        **{
            "label": "ELASTIC_CAFILE",
            "value": elastic.cafile,
            "desc": "Default: None. Elastic CA file. Search for elastic authentication for more information on how "
                    "to configure connection to elastic."
        }
    ),
    SystemSettings(
        **{
            "label": "ELASTIC_API_KEY",
            "value": elastic.api_key,
            "desc": "Default: None. Elastic API key. Search for elastic authentication for more information on how "
                    "to configure connection to elastic."
        }
    ),
    SystemSettings(
        **{
            "label": "ELASTIC_CLOUD_ID",
            "value": elastic.cloud_id,
            "desc": "Default: None. Search for elastic authentication for more information on how to configure "
                    "connection to elastic."
        }
    ),
    SystemSettings(
        **{
            "label": "ELASTIC_MAX_CONN",
            "value": elastic.maxsize,
            "desc": "Default: None. Defines max connection to elastic cluster. It defaults to elastic default value."
        }
    ),
    SystemSettings(
        **{
            "label": "ELASTIC_HTTP_COMPRESS",
            "value": elastic.http_compress,
            "desc": "default value: None. Set compression on data when the client calls the server."
        }
    ),
    SystemSettings(
        **{
            "label": "ELASTIC_VERIFY_CERTS",
            "value": elastic.verify_certs,
            "desc": "default value: None. Verify certificates when https schema is set. Set it to no if certificates "
                    "has no CA."
        }
    ),
    SystemSettings(
        **{
            "label": "ELASTIC_REFRESH_PROFILES_AFTER_SAVE",
            "value": elastic.refresh_profiles_after_save,
            "desc": "Default: no. When set to yes profile index will be forced to refresh its data after each update. "
                    "That means that elastic will write all updates without buffering. This may slow the elastic "
                    "significantly so be cautious with this setting."
        }
    ),
    SystemSettings(
        **{
            "label": "ELASTIC_LOGGING_LEVEL",
            "value": elastic.logging_level,
            "desc": "Default WARNING. Sets logging level of elastic requests. It may be useful to set it to INFO when"
                    " debugging Tracardi."
        }
    ),
    SystemSettings(
        **{
            "label": "REDIS_HOST",
            "value": redis_config.redis_host,
            "desc": "Default: redis://localhost:6379. This setting is used only when SYNC_PROFILE_TRACKS is equal to "
                    "yes. This is the host URI of Redis instance that is required to synchronize profile tracks. "
                    "Available only in commercial version of Tracardi."
        }
    ),
    SystemSettings(
        **{
            "label": "REDIS_PASSWORD",
            "value": "Set" if redis_config.redis_password is not None else "Unset",
            "desc": "Default: None. This is Redis password."
        }
    ),
    SystemSettings(
        **{
            "label": "TAGS_TTL",
            "value": memory_cache.tags_ttl,
            "desc": "Time of availability of event tags in memory cache, expressed in seconds, defaults to 60 seconds."
        }
    ),
    SystemSettings(
        **{
            "label": "EVENT_VALIDATOR_TTL",
            "value": memory_cache.event_validator_ttl,
            "desc": "How many seconds it takes to reload event validation schema. Validation JSON SCHEMA is cached for "
                    "performance reasons, defaults to 180 seconds."
        }
    ),
    SystemSettings(
        **{
            "label": "TOKENS_IN_REDIS",
            "value": tracardi.tokens_in_redis,
            "desc": "If set to 'yes', then user auth tokens are being cached on Redis. It allows multiple sessions for "
                    "one user and increases performance of the API. Defaults to 'yes'."
        }
    ),
    SystemSettings(
        **{
            "label": "SAVE_LOGS",
            "value": tracardi.save_logs,
            "desc": "Default: yes. When set to yes all logs will be saved n tracardi log."
        }
    ),
    SystemSettings(
        **{
            "label": "MONITOR_LOGS_EVENT_TYPE",
            "value": tracardi.monitor_logs_event_type,
            "desc": "Default: None. When set to any string all logs will converted into events with event type equal "
                    "to the string you set in MONITOR_LOGS_EVENT_TYPE."
        }
    ),
]

router = APIRouter(
    dependencies=[Depends(Permissions(roles=["admin", "developer"]))]
)


@router.get("/setting/{name}", tags=["settings"],
            include_in_schema=server.expose_gui_api,
            response_model=Optional[SystemSettings])
async def get_system_settings(name: str) -> Optional[SystemSettings]:
    """
    Returns setting with given name (str)
    """
    for setting in system_settings:
        if setting.label == name:
            return setting
    return None


@router.get("/settings", tags=["settings"],
            include_in_schema=server.expose_gui_api,
            response_model=List[SystemSettings])
async def get_system_settings() -> List[SystemSettings]:
    """
    Lists all system settings
    """
    return system_settings
