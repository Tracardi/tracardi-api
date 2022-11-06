import logging
from tracardi.config import tracardi
from tracardi.exceptions.log_handler import log_handler
from ..auth.user_db import token2user
from fastapi.security import OAuth2PasswordBearer
from tracardi.domain.user import User
from tracardi.exceptions.exception import LoginException
from tracardi.service.storage.driver import storage

_singleton = None
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/token")

logger = logging.getLogger(__name__)
logger.setLevel(tracardi.logging_level)
logger.addHandler(log_handler)


class Authentication:

    @staticmethod
    async def _authorize(username, password) -> User:  # username exists
        logger.info(f"Authorizing {username}...")

        user = await storage.driver.user.get_by_credentials(
            email=username,
            password=password
        )  # type: User

        if user is None:
            await storage.driver.user_log.add_log(email=username, successful=False)
            raise LoginException("Incorrect username or password.")

        if user.disabled:
            await storage.driver.user_log.add_log(email=username, successful=False)
            raise LoginException("This account was disabled")

        if user.is_expired():
            await storage.driver.user_log.add_log(email=username, successful=False)
            raise LoginException("This account has expired.")

        await storage.driver.user_log.add_log(email=username, successful=True)

        return user

    async def login(self, email, password):
        user = await self._authorize(email, password)

        # save token, match token with user in token2user
        token = token2user.set(user)

        return {"access_token": token, "token_type": "bearer", "roles": user.roles, "preference": user.preference}

    @staticmethod
    def logout(token):
        token2user.delete(token)


def get_authentication():
    global _singleton

    def get_auth():
        return Authentication()

    if _singleton is None:
        _singleton = get_auth()

    return _singleton
