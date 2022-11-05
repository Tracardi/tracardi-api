import json
import logging
from typing import Optional

from app.api.auth.token_memory import TokenMemory
from tracardi.config import tracardi
from tracardi.domain.user import User
from tracardi.exceptions.log_handler import log_handler
from hashlib import sha1

logger = logging.getLogger(__name__)
logger.setLevel(tracardi.logging_level)
logger.addHandler(log_handler)


class TokenDb:

    def __init__(self):
        self._token_memory = TokenMemory()

    def delete(self, token: str):
        del self._token_memory[token]

    def get(self, token: str) -> Optional[User]:
        user = self._token_memory[token]
        if user:
            user = json.loads(user)
            user = User(**user)
            user.token = token
            return user

        return None

    def set(self, token, user: User):
        self._token_memory[token] = user.json()

    def update(self, user: User) -> None:
        for key in self._token_memory.get_keys_by_email_hash(sha1(user.email.encode("utf-8")).hexdigest()):
            self._token_memory[key] = user.json()

    def refresh_token(self, token) -> None:
        self._token_memory.refresh(token)


token2user = TokenDb()
