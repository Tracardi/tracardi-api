import os
from app.config import server
from fastapi import APIRouter
from fastapi import Response

router = APIRouter()
_local_dir = os.path.dirname(__file__)


@router.get("/livechat/{license}", tags=["livechat"], include_in_schema=server.expose_gui_api)
async def livechat_script(license: str):
    """
    Returns livechat script
    """

    with open(os.path.join(_local_dir, 'livechat/snippet.js'), encoding='utf8') as f:
        snippet = f.read()

        return Response(
            snippet.replace("###LICENSE###", license),
            media_type="application/javascript; charset=utf-8",
            status_code=200,
            headers={
                'Cache-Control': 'max-age=2628000, must-revalidate'  # 1 month
            }
        )


@router.get("/chatwoot/{token}", tags=["chatwoot"], include_in_schema=server.expose_gui_api)
async def livechat_script(token: str):
    """
    Returns chatwoot script
    """

    with open(os.path.join(_local_dir, 'chatwoot/snippet.js'), encoding='utf8') as f:
        snippet = f.read()

        return Response(
            snippet.replace("###TOKEN###", token),
            media_type="application/javascript; charset=utf-8",
            status_code=200,
            headers={
                'Cache-Control': 'max-age=2628000, must-revalidate'  # 1 month
            }
        )


@router.get("/intercom/{app_id}", tags=["intercom"], include_in_schema=server.expose_gui_api)
async def intercom_script(app_id: str):
    """
    Returns intercom script
    """

    with open(os.path.join(_local_dir, "intercom/snippet.js"), encoding='utf8') as f:
        snippet = f.read()

        return Response(
            snippet.replace("###APP_ID###", app_id),
            media_type="application/javascript; charset=utf-8",
            status_code=200,
            headers={
                'Cache-Control': 'max-age=2628000, must-revalidate'  # 1 month
            }
        )
