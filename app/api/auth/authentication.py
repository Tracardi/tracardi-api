from tracardi.domain import ExtraInfo
from tracardi.exceptions.log_handler import get_logger
from tracardi.service.storage.mysql.service.user_service import UserService
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
        logger.debug(
            f"Authorizing {username}...",
            extra=ExtraInfo.exact(
                "Authentication",
                class_name="Authentication",
                package=__name__,
                user_id=username
            )
        )

        try:
            us = UserService()
            user: User = await us.load_by_credentials(
                    email=username,
                    password=password
                )
        except Exception as e:
            raise LoginException(f"System not installed. Got error {str(e)}")

        if user is None:
            logger.warning(
                "Incorrect username or password.",
                extra=ExtraInfo.exact(
                    origin="authentication",
                    class_name=Authentication,
                    package=__name__,
                    user_id=username
                )
            )
            raise LoginException("Incorrect username or password.")

        if not user.enabled:
            logger.warning(
                "This account was disabled.",
                extra=ExtraInfo.exact(
                    origin="authentication",
                    class_name=Authentication,
                    package=__name__,
                    user_id=username
                )
            )
            raise LoginException("This account was disabled")

        if user.is_expired():
            logger.warning(
                "This account has expired.",
                extra=ExtraInfo.exact(
                    origin="authentication",
                    class_name=Authentication,
                    package=__name__,
                    user_id=username
                )
            )
            raise LoginException("This account has expired.")

        logger.info(
            "User logged-in.",
            extra=ExtraInfo.exact(
                origin="authentication",
                class_name="Authentication",
                package=__name__,
                user_id=username
            )
        )
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
