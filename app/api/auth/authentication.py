from tracardi.exceptions.log_handler import get_logger
from tracardi.service.storage.driver.elastic import user_log as user_log_db
from tracardi.service.storage.driver.elastic import user as user_db
from ..auth.user_db import token2user
from fastapi.security import OAuth2PasswordBearer
from tracardi.domain.user import User
from tracardi.exceptions.exception import LoginException


_singleton = None
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/token")

logger = get_logger(__name__)


class Authentication:

    @staticmethod
    async def _authorize(username, password) -> User:  # username exists
        logger.info(f"Authorizing {username}...")

        try:
            user = await user_db.get_by_credentials(
                email=username,
                password=password
            )  # type: User
        except Exception as e:
            raise LoginException(f"System not installed. Got error {str(e)}")

        if user is None:
            await user_log_db.add_log(email=username, successful=False)
            raise LoginException("Incorrect username or password.")

        if user.disabled:
            await user_log_db.add_log(email=username, successful=False)
            raise LoginException("This account was disabled")

        if user.is_expired():
            await user_log_db.add_log(email=username, successful=False)
            raise LoginException("This account has expired.")

        await user_log_db.add_log(email=username, successful=True)

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
