import logging

from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer

from app.api.auth.user_db import token2user
from app.config import server
from tracardi.config import tracardi
from tracardi.exceptions.log_handler import log_handler

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/token")

logger = logging.getLogger(__name__)
logger.setLevel(tracardi.logging_level)
logger.addHandler(log_handler)


class Permissions:

    def __init__(self, roles):
        self.roles = roles

    async def __call__(self, request: Request, token: str = Depends(oauth2_scheme)):

        if not server.expose_gui_api or token is None:
            if not server.expose_gui_api:
                logger.warning("Unauthorized access to disabled API.")
            else:
                logger.warning("Unauthorized access with empty token.")

            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access forbidden",
            )

        user = token2user.get(token)

        # Not authenticated if no user or insufficient roles

        if not user:
            logger.warning(f"Unauthorized access. User not available for {token}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

        refreshed_token = token2user.refresh(user)

        if refreshed_token != token:
            token2user.delete(token)
            token2user.delete(refreshed_token)

            logger.warning(f"Unauthorized access. User token mismatch {token} != {refreshed_token}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

        if not user.has_roles(self.roles):
            logger.warning(f"User {user.email}. Unauthorized access to {request.url}. Required roles {self.roles}, "
                           f"granted {user.roles} ")

            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return user
