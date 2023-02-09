from tracardi.config import tracardi
from tracardi.context import Context, ServerContext
from starlette.types import ASGIApp, Receive, Scope, Send
from app.api.auth.user_db import token2user


def _get_context_object(scope) -> Context:
    production = tracardi.version.production
    token = ''
    headers = scope.get('headers', None)

    if headers:
        for header, value in headers:
            if header.decode() == "x-context":
                context = value.decode()
                # if has some value
                if context and context in ['production', 'staging']:
                    production = context.lower() == 'production'
            elif header.decode() == 'authorization':
                token = value.decode()

    ctx = Context(production=production)
    if scope.get('method', None) != "options":
        if token:
            _, token = token.split()
            ctx.user = token2user.get(token)

    return ctx


class CustomRequestMiddleware:
    def __init__(
            self,
            app: ASGIApp,
    ) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] not in ["http", "websocket", "https"]:
            await self.app(scope, receive, send)
            return

        context_object = _get_context_object(scope)
        with ServerContext(context_object):
            await self.app(scope, receive, send)
