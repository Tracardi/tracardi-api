from typing import Union, List

from app.api.auth.authentication import get_current_user
from app.config import *
from fastapi import APIRouter, Depends
from pydantic import BaseModel


class SystemSettings(BaseModel):
    label: str
    value: Union[str, int, float, bool]
    desc: str


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
]

router = APIRouter(
    dependencies=[Depends(get_current_user)]
)


@router.get("/settings", tags=["settings"],
            include_in_schema=server.expose_gui_api,
            response_model=List[SystemSettings])
async def get_system_settings() -> List[SystemSettings]:
    return system_settings
