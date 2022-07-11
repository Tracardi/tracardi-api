from typing import List, Optional
from pydantic import BaseModel, validator
from tracardi.service.valiadator import validate_email
from pytimeparse import parse
from datetime import datetime


class UserPayload(BaseModel):
    password: str
    full_name: str
    email: str
    roles: List[str]
    disabled: bool = False
    expiration_offset: Optional[str] = None

    @validator("email")
    def validate_email(cls, value):
        if not validate_email(value):
            raise ValueError("Given e-mail is invalid.")
        return value

    @validator("expiration_offset")
    def validate_expiration_offset(cls, value):
        if value is not None and parse(value) is None:
            raise ValueError("Given expiration offset is invalid.")
        return value

    def get_expiration_date(self) -> int:
        return None if self.expiration_offset is None else \
            int(parse(self.expiration_offset) + datetime.utcnow().timestamp())

    def has_admin_role(self):
        return "admin" in self.roles
