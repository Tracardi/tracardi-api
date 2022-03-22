import logging
import secrets
from typing import Optional

from tracardi.config import tracardi
from tracardi.exceptions.log_handler import log_handler
from ..auth.user_db import token2user
from fastapi.security import OAuth2PasswordBearer
from tracardi.domain.user import User
from ...config import auth
from tracardi.exceptions.exception import LoginException
from tracardi.service.storage.driver import storage

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

        if auth.user is not None and username == auth.user and password == auth.password:
            user = User(
                        id=auth.user,
                        password=auth.password,
                        roles=['admin'],
                        email=auth.user,
                        full_name="John Doe"
                    )
            if not await storage.driver.user.check_if_exists(auth.user):
                await storage.driver.user.add_user(user)
                logger.warning(f"Account {username} created with provided password. Please change password.")

            await storage.driver.user_log.add_log(email=username, successful=False)

            logger.warning(f"Account {username} has default password. Please change password.")

            return user

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

        await storage.driver.user_log.add_log(email=username, successful=True)

        return user

    @staticmethod
    def _generate_token():
        return secrets.token_hex(32)

    async def login(self, email, password):
        user = await self.authorize(email, password)
        token = self._generate_token()

        # save token, match token with user in token2user
        await self.token2user.set(email, token)

        return {"access_token": token, "token_type": "bearer", "roles": user.roles}

    async def logout(self, token):
        await self.token2user.delete(token)

    async def get_user_by_token(self, token) -> Optional[User]:
        return await self.token2user.get(token)


def get_authentication():
    global _singleton

    def get_auth():
        return Authentication()

    if _singleton is None:
        _singleton = get_auth()

    return _singleton


# async def get_current_user(request: Request, token: str = Depends(oauth2_scheme)):
#
#     if not server.expose_gui_api:
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="Access forbidden",
#         )
#
#     try:
#         auth = Authentication()
#         user = await auth.get_user_by_token(token)
#     except ElasticsearchException as e:
#         logger.error(str(e))
#         raise HTTPException(
#                 status_code=status.HTTP_403_FORBIDDEN,
#                 detail=str(e)
#             )
#     except Exception as e:
#         logger.error(str(e))
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="Access forbidden",
#         )
#
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid authentication credentials",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     return user
