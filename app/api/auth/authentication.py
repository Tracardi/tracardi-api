import logging
import secrets
from typing import Optional

from tracardi.config import tracardi
from tracardi.exceptions.log_handler import log_handler
from ..auth.user_db import token2user
from fastapi.security import OAuth2PasswordBearer
from tracardi.domain.user import User
from tracardi.exceptions.exception import LoginException
from tracardi.service.storage.driver import storage
from hashlib import sha1

_singleton = None
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

logger = logging.getLogger(__name__)
logger.setLevel(tracardi.logging_level)
logger.addHandler(log_handler)


class Authentication:

    def __init__(self):
        self.token2user = token2user

    @staticmethod
    async def authorize(username, password) -> User:  # username exists
        logger.info(f"Authorizing {username}...")

        user = await storage.driver.user.get_by_credentials(
            email=username,
            password=password
        )

        if user is None:
            await storage.driver.user_log.add_log(email=username, successful=False)
            raise LoginException("Incorrect username or password.")

        if user.disabled:
            await storage.driver.user_log.add_log(email=username, successful=False)
            raise ValueError("This account was disabled")

        if user.is_expired():
            await storage.driver.user_log.add_log(email=username, successful=False)
            raise ValueError("This account has expired.")

        await storage.driver.user_log.add_log(email=username, successful=True)

        return user

    @staticmethod
    def _generate_token():
        return secrets.token_hex(32)

    async def login(self, email, password):
        user = await self.authorize(email, password)
        token = f"{sha1(user.email.encode('utf-8')).hexdigest()}-{self._generate_token()}"

        # save token, match token with user in token2user
        await self.token2user.set(token, user)

        return {"access_token": token, "token_type": "bearer", "roles": user.roles}

    async def logout(self, token):
        await self.token2user.delete(token)

    async def get_user_by_token(self, token) -> Optional[User]:
        return await self.token2user.get(token)

    async def refresh_token(self, token) -> None:
        await self.token2user.refresh_token(token)


def get_authentication():
    global _singleton

    def get_auth():
        return Authentication()

    if _singleton is None:
        _singleton = get_auth()

    return _singleton
