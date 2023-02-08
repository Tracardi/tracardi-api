from starlette.types import ASGIApp, Receive, Scope, Send

from app.api.auth.user_db import token2user
from tracardi.context import ctx_var, Context


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

        context = 'staging'
        token = ''
        headers = scope.get('headers', None)

        if headers:
            for header, value in headers:
                if header.decode() == "x-context":
                    context = value.decode()
                elif header.decode() == 'authorization':
                    token = value.decode()

        ctx = Context(scope=context)

        if context == 'production':
            if scope.get('method', None) != "options":
                if token:
                    _, token = token.split()
                    ctx.user = token2user.get(token)

        context = ctx_var.set(ctx)

        await self.app(scope, receive, send)

        ctx_var.reset(context)
