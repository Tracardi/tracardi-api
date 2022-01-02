from collections import defaultdict

from fastapi import APIRouter
from fastapi import HTTPException, Depends

from tracardi.service.storage.driver import storage
from .auth.authentication import get_current_user
from app.service.grouper import search
from tracardi.domain.resource import Resource
from ..config import server

router = APIRouter(
    dependencies=[Depends(get_current_user)]
)


@router.get("/credentials/by_type", tags=["credential"], include_in_schema=server.expose_gui_api)
async def get_credentials(query: str = None, limit: int = 500):
    try:
        result, total = await storage.driver.resource.load_all(limit=limit)

        # Filtering
        if query is not None and len(query) > 0:
            query = query.lower()
            if query:
                result = [r for r in result if query in r.name.lower() or search(query, r.type)]

        # Grouping
        groups = defaultdict(list)
        for source in result:  # type: Resource
            if isinstance(source.type, list):
                for group in source.type:
                    groups[group].append(source)
            elif isinstance(source.type, str):
                groups[source.type].append(source)

        # Sort
        groups = {k: sorted(v, key=lambda r: r.name, reverse=False) for k, v in groups.items()}

        return {
            "total": total,
            "grouped": groups
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
