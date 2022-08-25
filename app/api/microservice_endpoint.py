from typing import Type, Dict, Tuple, Optional
from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, ValidationError
from starlette.responses import JSONResponse

from app.config import server
from app.service.error_converter import convert_errors
from tracardi.process_engine.action.v1.connectors.trello.add_card_action.model.config import Config
from tracardi.process_engine.action.v1.connectors.trello.add_card_action.plugin import TrelloCardAdder
from tracardi.service.plugin.domain.register import Form, FormGroup, FormField, FormComponent, Plugin, Spec, MetaData, \
    Documentation, PortDoc
from tracardi.service.plugin.runner import ActionRunner


class PluginExecContext(BaseModel):
    context: dict
    params: dict
    init: dict


class PluginConfig(BaseModel):
    name: str
    validator: Type[BaseModel]
    plugin: Type[ActionRunner]
    registry: Plugin


class ServiceConfig(BaseModel):
    name: str
    microservice: Plugin  # ? registry
    plugins: Dict[str, PluginConfig]


class ServicesRepo(BaseModel):
    repo: Dict[str, ServiceConfig]

    def get_all_services(self) -> Tuple[str, str]:
        for id, service in self.repo.items():
            yield id, service.name

    def get_all_action_plugins(self, service_id: str) -> Tuple[str, str]:
        if service_id in self.repo:
            service = self.repo[service_id]
            for id, plugin_config in service.plugins.items():
                yield id, plugin_config.name

    def get_plugin_microservice_plugin_registry(self, service_id: str) -> Optional[Plugin]:
        if service_id in self.repo:
            service = self.repo[service_id]
            return service.microservice
        return None

    def get_plugin(self, service_id: str, plugin_id: str) -> Optional[Type[ActionRunner]]:
        if service_id in self.repo:
            service = self.repo[service_id]
            if plugin_id in service.plugins:
                plugin_config = service.plugins[plugin_id]
                return plugin_config.plugin
        return None

    def get_plugin_registry(self, service_id: str) -> Optional[Plugin]:
        if service_id in self.repo:
            service = self.repo[service_id]
            return service.microservice
        return None

    def get_plugin_form_an_init(self, service_id: str, plugin_id: str) -> Tuple[Optional[dict], Optional[Form]]:
        if service_id in self.repo:
            service = self.repo[service_id]
            if plugin_id in service.plugins:
                plugin_config = service.plugins[plugin_id]
                return plugin_config.registry.spec.init, plugin_config.registry.spec.form
        return None, None

    def get_plugin_validator(self, service_id: str, plugin_id: str) -> Type[BaseModel]:
        if service_id in self.repo:
            service = self.repo[service_id]
            if plugin_id in service.plugins:
                plugin_config = service.plugins[plugin_id]
                return plugin_config.validator
        raise LookupError(f"Missing validator configuration for service {service_id} and plugin {plugin_id}")


repo = ServicesRepo(
    repo={
        "a307b281-2629-4c12-b6e3-df1ec9bca35a": ServiceConfig(
            name="Trello",
            microservice=Plugin(
                start=False,
                spec=Spec(
                    module='tracardi.process_engine.action.v1.microservice.plugin',
                    className='MicroserviceAction',
                    inputs=["payload"],
                    outputs=["payload", "error"],
                    version='0.7.2',
                    license="MIT",
                    author="Risto Kowaczewski",
                ),
                metadata=MetaData(
                    name='Trello Microservice',
                    desc='Microservice that runs Trello plugins.',
                    icon='trello',
                    group=["Connectors"],
                    remote=True,
                    documentation=Documentation(
                        inputs={
                            "payload": PortDoc(desc="This port takes payload object.")
                        },
                        outputs={
                            "payload": PortDoc(desc="This port returns microservice response.")
                        }
                    )
                )),
            plugins={
                "a04381af-c008-4328-ab61-0e73825903ce": PluginConfig(
                    name="Add card 1",
                    validator=Config,
                    plugin=TrelloCardAdder,
                    registry=Plugin(
                        start=False,
                        spec=Spec(
                            module='plugins.trello.add_card.plugin',
                            className='TrelloCardAdder',
                            inputs=["payload"],
                            outputs=["response", "error"],
                            version='0.6.1',
                            license="MIT",
                            author="Dawid Kruk",
                            manual="trello/add_trello_card_action",
                            init={
                                "source": {
                                    "name": None,
                                    "id": None
                                },
                                "board_url": "",
                                "list_name": "",
                                "card": {
                                    "name": "",
                                    "desc": "",
                                    "urlSource": "",
                                    "coordinates": "",
                                    "due": ""
                                }

                            },
                            form=Form(
                                groups=[
                                    FormGroup(
                                        name="Plugin configuration",
                                        fields=[
                                            FormField(
                                                id="source",
                                                name="Trello resource",
                                                description="Please select your Trello resource.",
                                                component=FormComponent(type="resource",
                                                                        props={"label": "Resource", "tag": "trello"})
                                            ),
                                            FormField(
                                                id="board_url",
                                                name="URL of Trello board",
                                                description="Please the URL of your board.",
                                                component=FormComponent(type="text", props={"label": "Board URL"})
                                            ),
                                            FormField(
                                                id="list_name",
                                                name="Name of Trello list",
                                                description="Please provide the name of your Trello list.",
                                                component=FormComponent(type="text", props={"label": "List name"})
                                            ),
                                            FormField(
                                                id="card.name",
                                                name="Name of your card",
                                                description="Please provide path to the name of the card that you want to add.",
                                                component=FormComponent(type="dotPath", props={"label": "Card name",
                                                                                               "defaultMode": "2"})
                                            ),
                                            FormField(
                                                id="card.desc",
                                                name="Card description",
                                                description="Please provide description of your card. It's fully functional in terms of"
                                                            " using templates.",
                                                component=FormComponent(type="textarea",
                                                                        props={"label": "Card description"})
                                            ),
                                            FormField(
                                                id="card.urlSource",
                                                name="Card link",
                                                description="You can add an URL to your card as an attachment.",
                                                component=FormComponent(type="dotPath", props={"label": "Card link",
                                                                                               "defaultMode": "2"})
                                            ),
                                            FormField(
                                                id="card.coordinates",
                                                name="Card coordinates",
                                                description="You can add location coordinates to your card. This should be a path"
                                                            " to an object, containing 'longitude' and 'latitude' fields.",
                                                component=FormComponent(type="dotPath",
                                                                        props={"label": "Card coordinates",
                                                                               "defaultMode": "2"})
                                            ),
                                            FormField(
                                                id="card.due",
                                                name="Card due date",
                                                description="You can add due date to your card. Various formats should work, but "
                                                            "UTC format seems to be the best option.",
                                                component=FormComponent(type="dotPath",
                                                                        props={"defaultMode": "2",
                                                                               "label": "Card due date"})
                                            )
                                        ]
                                    )
                                ]
                            )
                        ),
                        # todo this may be not need
                        metadata=MetaData(
                            name='Add Trello card',
                            desc='Adds card to given list on given board in Trello.',
                            icon='trello',
                            group=["Trello"],
                            documentation=Documentation(
                                inputs={
                                    "payload": PortDoc(desc="This port takes payload object.")
                                },
                                outputs={
                                    "response": PortDoc(desc="This port returns a response from Trello API."),
                                    "error": PortDoc(desc="This port gets triggered if an error occurs.")
                                }
                            ),
                            pro=True
                        )
                    )
                )
            }
        )
    })

router = APIRouter()


@router.get("/services", tags=["microservice"], include_in_schema=server.expose_gui_api, response_model=dict)
async def get_all_services():
    services = list(repo.get_all_services())
    return {
        "total": len(services),
        "result": {id: name for id, name in services}
    }


@router.get("/actions", tags=["microservice"], include_in_schema=server.expose_gui_api, response_model=dict)
async def get_actions(service_id: str):
    actions = list(repo.get_all_action_plugins(service_id))
    return {
        "total": len(actions),
        "result": {id: name for id, name in actions}
    }


@router.get("/plugin/form", tags=["microservice"], include_in_schema=server.expose_gui_api, response_model=dict)
async def get_plugin(service_id: str, action_id: str):
    init, form = repo.get_plugin_form_an_init(service_id, action_id)

    return {
        "init": init if init is not None else {},
        "form": form.dict() if form is not None else None
    }


@router.get("/plugin/registry", tags=["microservice"], include_in_schema=server.expose_gui_api, response_model=Plugin)
async def get_plugin_registry(service_id: str):
    return repo.get_plugin_registry(service_id)


@router.post("/plugin/validate", tags=["microservice"], include_in_schema=server.expose_gui_api, response_model=dict)
async def validate_plugin_configuration(service_id: str, action_id: str, data: dict):
    try:
        validator = repo.get_plugin_validator(service_id, action_id)
        return validator(**data)
    except ValidationError as e:
        return JSONResponse(
            status_code=422,
            content=jsonable_encoder(convert_errors(e))
        )


@router.post("/plugin/run", tags=["microservice"], include_in_schema=server.expose_gui_api, response_model=dict)
async def validate_plugin_configuration(service_id: str, action_id: str, data: PluginExecContext):
    try:
        plugin = repo.get_plugin(service_id, action_id)
        print(data.init)
        if plugin:
            plugin = await plugin.build(**data.init)
            print(await plugin.run(**data.params))
        return {}
    except ValidationError as e:
        return JSONResponse(
            status_code=422,
            content=jsonable_encoder(convert_errors(e))
        )
