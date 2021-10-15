from typing import List, Union
from app.config import *
from fastapi import APIRouter
from pydantic import BaseModel


class EnvVar(BaseModel):
    suffix: str
    label: str
    value: Union[str, int, float, bool]
    desc: str

    def generate_endpoint(self):
        return "/settings/{}".format(self.suffix)


def get_envs() -> List[EnvVar]:
    env_vars = [
        EnvVar(
            **{
                "label": "USER_NAME",
                "variable": ("user", auth.user),
                "desc": "Environmental variable containing username."
            }
        ),
        EnvVar(
            **{
                "label": "PASSWORD",
                "variable": ("password", auth.password),
                "desc": "Environmental variable containing password."
            }
        ),
        EnvVar(
            **{
                "label": "UPDATE_PLUGINS_ON_STARTUP",
                "variable": ("update_plugins_on_startup", server.update_plugins_on_start_up),
                "desc": "Environmental variable telling TracardiAPI to update plugins on startup or not."
            }
        ),
        EnvVar(
            **{
                "label": "DEBUG_MAKE_SLOWER_RESPONSES",
                "variable": ("make_slower_responses", server.make_slower_responses),
                "desc": "Environmental variable telling TracardiAPI the speed of debug responses, defaults to 0."
            }
        ),
        EnvVar(
            **{
                "label": "RUN_HEARTBEAT_EVERY",
                "variable": ("heartbeat_every", server.heartbeat_every),
                "desc": "Environmental variable telling TracardiAPI the interval of running heartbeat in seconds, "
                        "defaults to 300."
            }
        ),
        EnvVar(
            **{
                "label": "TASKS_EVERY",
                "variable": ("tasks_every", server.tasks_every),
                "desc": "Environmental variable telling TracardiAPI the interval of running tasks in seconds, "
                        "defaults to 1."
            }
        ),
        EnvVar(
            **{
                "label": "AUTOLOAD_PAGE_SIZE",
                "variable": ("page_size", server.page_size),
                "desc": "Environmental variable telling TracardiAPI the size of automatically loaded page, defaults"
                        " to 25."
            }
        ),
        EnvVar(
            **{
                "label": "EXPOSE_GUI_API",
                "variable": ("expose_gui_api", server.expose_gui_api),
                "desc": "Environmental variable telling TracardiAPI to expose GUI API or not, defaults to True, "
                        "can be changed by setting this variable to 'yes' (then it's True) or something else, "
                        "which makes it False."
            }
        ),
        EnvVar(
            **{
                "label": "RESET_PLUGINS",
                "variable": ("reset_plugins", server.reset_plugins),
                "desc": "Environmental variable telling TracardiAPI to reset plugins data in ElasticSearch database"
                        " or not to do so, defaults to False, can be changed as previous one."
            }
        ),
    ]
    return env_vars


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
