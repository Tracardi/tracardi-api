from typing import List
from pydantic import BaseModel, validator
from tracardi.service.valiadator import validate_email


class UserPayload(BaseModel):
    password: str
    full_name: str
    email: str
    roles: List[str]
    disabled: bool = False

    @validator("email")
    def validate_email(cls, value):
        if not validate_email(value):
            raise ValueError("Given e-mail is invalid.")
        return value

    def has_admin_role(self):
        return "admin" in self.roles
