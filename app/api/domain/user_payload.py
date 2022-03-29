import re
from typing import List

from pydantic import BaseModel, validator

from app.config import auth


class UserPayload(BaseModel):
    password: str
    full_name: str
    email: str
    roles: List[str]
    disabled: bool = False

    @validator("email")
    def validate_email(cls, value):
        if value == auth.user:
            raise ValueError("You cannot edit default admin account")
        if not re.fullmatch(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+', value):
            raise ValueError("Given email is invalid.")
        return value

    def has_admin_role(self):
        return "admin" in self.roles
