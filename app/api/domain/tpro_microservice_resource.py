from typing import Optional

from pydantic import BaseModel
from tracardi.domain.named_entity import NamedEntity


class TProMicroserviceCredentials(BaseModel):
    url: str
    token: str

    def is_configured(self) -> bool:
        return bool(self.url and self.token)


class TProMicroserviceResource(BaseModel):
    service: NamedEntity
    credentials: Optional[dict] = {}
