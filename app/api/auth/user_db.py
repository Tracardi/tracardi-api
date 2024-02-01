import json
from hashlib import sha1
from typing import Optional

from app.api.auth.token_memory import TokenMemory
from tracardi.domain.user import User
from tracardi.exceptions.log_handler import get_logger

logger = get_logger(__name__)


class TokenDb:

    def __init__(self):
        self._token_memory = TokenMemory()
        self.salt = "fe-skd~jS(ADsd-9328r&aS5ZFGdaF-STREas4TA"

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
