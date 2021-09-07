from typing import Optional
from fastapi import APIRouter
from fastapi import HTTPException, Depends
from fastapi.responses import Response
from tracardi.domain.session import Session
from tracardi.service.storage.factory import StorageFor
from .auth.authentication import get_current_user

router = APIRouter(
    dependencies=[Depends(get_current_user)]
)


@router.get("/session/{id}", tags=["session"], response_model=Optional[Session])
async def get_profile_by_id(id: str, response: Response):
    try:
        session = Session(id=id)
        result = await StorageFor(session).index().load()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    print(result)
    if result is None:
        response.status_code = 404

    return result
