import secrets
from elasticsearch import ElasticsearchException
from ..auth.user_db import token2user
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from starlette import status
from tracardi.service.login_service import find_user

from ...config import server

_singleton = None
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class Authentication:

    def __init__(self):
        self.token2user = token2user

    async def authorize(self, username, password):  # username exists

        user = await find_user(username, password)

        if user.disabled:
            raise ValueError("This account was disabled")

        return user

    @staticmethod
    def _generate_token():
        return secrets.token_hex(32)

    async def login(self, username, password):
        user = await self.authorize(username, password)
        token = self._generate_token()
        # save token, match token with user in token2user
        await self.token2user.set(token, username)

        return {"access_token": token, "token_type": "bearer", "roles": user.roles}

    async def logout(self, token):
        await self.token2user.delete(token)

    async def get_user_by_token(self, token):
        if await self.token2user.has(token):
            return await self.token2user.get(token)
        else:
            return None


def get_authentication():
    global _singleton

    def get_auth():
        return Authentication()

    if _singleton is None:
        _singleton = get_auth()

    return _singleton


async def get_current_user(token: str = Depends(oauth2_scheme)):

    if not server.expose_gui_api:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access forbidden",
        )

    try:
        auth = Authentication()
        user = await auth.get_user_by_token(token)
    except ElasticsearchException as e:
        raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=str(e)
            )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access forbidden",
        )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user
