import re
from tracardi.config import tracardi
from tracardi.context import Context, ServerContext
from starlette.types import ASGIApp, Receive, Scope, Send
from app.api.auth.user_db import token2user
from tracardi.service.tenant_manager import get_tenant_name_from_scope

pattern = re.compile(r'[^a-z]')


def _get_context_object(scope) -> Context:
    # Default context comes from evn variable PRODUCTION
    production = tracardi.version.production

    token = ''

    # If env variable set to PRODUCTION=yes there is no way to change it.
    # Production means production. Otherwise the context can be changed
    # form outside.

    tenant, hostname = get_tenant_name_from_scope(scope)

    if tenant is None:
        raise OSError("Can not find tenant for this URL. Tenant name can not be shorted then 3 letters and must "
                      f"not contain numbers. Scope: {scope}")

    if not production:  # Staging as default

        headers = scope.get('headers', None)

        # Context can be overridden by x-context header.
        if headers:
            for header, value in headers:
                if header.decode() == "x-context":
                    context = value.decode()
                    # if has some value
                    if context and context in ['production', 'staging']:
                        production = context.lower() == 'production'
                elif header.decode() == 'authorization':
                    token = value.decode()

    user = None
    if scope.get('method', None) != "options":
        if token:
            _, token = token.split()
            user = token2user.get(token)

    return Context(production=production, user=user, tenant=tenant, host=hostname)


class ContextRequestMiddleware:
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
