import re
from typing import Optional

from tracardi.config import tracardi
from tracardi.context import Context, ServerContext
from starlette.types import ASGIApp, Receive, Scope, Send
from app.api.auth.user_db import token2user

pattern = re.compile(r'[^a-z]')


def get_tenant_name(scope) -> Optional[str]:
    tenant = None
    if tracardi.multi_tenant:
        if 'headers' in scope:
            headers = {item[0].decode(): item[1].decode() for item in scope['headers']}
            if 'host' in headers:
                hostname = headers['host']
                if hostname not in ['localhost', '0.0.0.0', '127.0.0.1']:
                    hostname = hostname.split(":")[0]
                    parts = hostname.split(".")
                    if len(parts) >= 3:
                        _tenant_candidate = remove_non_alpha(parts[0])
                        if len(_tenant_candidate) >= 3 and not _tenant_candidate.isnumeric():
                            tenant = _tenant_candidate
    else:
        tenant = tracardi.version.name

    return tenant


def remove_non_alpha(text):
    # Use regular expression to match only lowercase letters
    cleaned_text = re.sub(pattern, '', text)
    return cleaned_text


def _get_context_object(scope) -> Context:
    # Default context comes from evn variable PRODUCTION
    production = tracardi.version.production

    token = ''

    # If env variable set to PRODUCTION=yes there is no way to change it.
    # Production means production. Otherwise the context can be changed
    # form outside.

    tenant = get_tenant_name(scope)

    if tenant is None:
        raise OSError("Can not find tenant for this instance. Tenant name can not be shorted then 3 letters and must "
                      "not contain numbers.")

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

    return Context(production=production, user=user, tenant=tenant)


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
