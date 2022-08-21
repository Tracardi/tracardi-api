from fastapi import APIRouter
from app.config import server
from tracardi.service.plugin.domain.register import Form, FormGroup, FormField, FormComponent

router = APIRouter()


@router.get("/services", tags=["microservice"], include_in_schema=server.expose_gui_api, response_model=dict)
async def get_services():
    return {
        "total": 2,
        "result": [
            {
                "id": 1,
                "name": "service 1"
            },
            {
                "id": 2,
                "name": "service 2"
            }
        ]

    }


@router.get("/actions", tags=["microservice"], include_in_schema=server.expose_gui_api, response_model=dict)
async def get_actions():
    return {
        "total": 2,
        "result": [
            {
                "id": 1,
                "name": "action 1"
            },
            {
                "id": 2,
                "name": "action 2"
            }
        ]
    }


@router.get("/plugin", tags=["microservice"], include_in_schema=server.expose_gui_api, response_model=dict)
async def get_plugin():

    form = Form(groups=[
                FormGroup(
                    name="Calculations",
                    description="Calculations are made in a simple domain specific language. "
                                "See documentation for details.",
                    fields=[
                        FormField(
                            id="calc_dsl",
                            name="Calculation equations",
                            description="One calculation per line. "
                                        "Example: profile@stats.counters.my_count = profile@stats.visits + 1",
                            component=FormComponent(type="textarea", props={"label": "Calculations"})
                        )
                    ]
                ),
            ])

    return {
        "init": {"calc_dsl": ""},
        "form": form.dict()
    }
