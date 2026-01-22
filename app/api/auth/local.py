import os

from fastapi import HTTPException, Request


# Localhost-only dependency for health checks
async def is_localhost_only(request: Request):
    """
    Ensures the request comes from localhost only.
    Health check endpoints should only be accessible from localhost for security.
    """
    client_host = request.client.host if request.client else None

    # Allow localhost, 127.0.0.1, and ::1 (IPv6 localhost)
    allowed_hosts = {"localhost", "127.0.0.1", "::1", "::ffff:127.0.0.1", os.environ.get("HEALTCHECK_ALLOWED_IP", "::1")}

    if client_host not in allowed_hosts:
        raise HTTPException(
            status_code=403,
            detail=f"Health endpoints are only accessible from localhost. Your IP: {client_host}"
        )

    return True
