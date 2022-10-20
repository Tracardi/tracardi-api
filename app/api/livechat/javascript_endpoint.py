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

    with open(os.path.join(_local_dir, 'javascript/snippet.js'), encoding='utf8') as f:
        snippet = f.read()

        return Response(
            snippet.replace("###LICENSE###", license),
            media_type="application/javascript; charset=utf-8",
            status_code=200,
            headers={
                'Cache-Control': 'max-age=2628000, must-revalidate'  # 1 month
            }
        )
