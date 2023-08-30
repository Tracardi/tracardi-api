import json
import logging
from hashlib import sha1
from typing import Optional

from app.api.auth.token_memory import TokenMemory
from tracardi.config import tracardi
from tracardi.domain.user import User
from tracardi.exceptions.log_handler import log_handler

logger = logging.getLogger(__name__)
logger.setLevel(tracardi.logging_level)
logger.addHandler(log_handler)


class TokenDb:

    def __init__(self):
        self._token_memory = TokenMemory()
        self.salt = "skdjsd9328r&"

    def _get_token(self, user: User) -> str:
        return sha1((user.id + self.salt).encode('utf-8')).hexdigest()

    def delete(self, token: str):
        del self._token_memory[token]

    def get(self, token: str) -> Optional[User]:
        user = self._token_memory[token]
        if user:
            user = json.loads(user)
            user = User(**user)
            return user

        return None

    def set(self, user: User) -> str:
        token = self._get_token(user)
        self._token_memory[token] = user.model_dump_json()
        return token

    def refresh(self, user: User) -> str:
        token = self._get_token(user)
        self._token_memory.refresh(token)
        return token


token2user = TokenDb()
