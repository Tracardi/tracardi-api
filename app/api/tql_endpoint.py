from fastapi import APIRouter, Request
from fastapi import HTTPException
from lark.exceptions import LarkError

from app.config import server
from tracardi.process_engine.tql.condition import Condition

router = APIRouter()


@router.post("/tql/validate", tags=["tql"], include_in_schema=server.expose_gui_api)
async def is_tql_valid(request: Request):
    try:
        tql = await request.body()
        condition = Condition()
        condition.parse(tql.decode('utf-8'))
        return True
    except LarkError as e:
        raise HTTPException(status_code=400, detail=str(e))