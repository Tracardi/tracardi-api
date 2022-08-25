from pydantic import BaseModel

from tracardi.domain.named_entity import NamedEntity


class TProMicroserviceCredentials(BaseModel):
    url: str
    token: str


class TProMicroserviceResource(BaseModel):
    service: NamedEntity
    credentials: TProMicroserviceCredentials
