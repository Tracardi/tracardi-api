from fastapi import Request, Response
from elasticsearch import ElasticsearchException
from fastapi.routing import APIRoute

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from starlette import status

from app.api.auth.authentication import Authentication
from app.config import server


class RestrictedRoute(APIRoute):
    def get_route_handler(self):
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
            token = await oauth2_scheme(request)
            print(self.path, token)

            if not server.expose_gui_api:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Access forbidden",
                )

            try:
                auth = Authentication()
                user = await auth.get_user_by_token(token)

                print("user", user)
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

            response: Response = await original_route_handler(request)

            return response

        return custom_route_handler
