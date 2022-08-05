from fastapi import APIRouter
from fastapi import HTTPException, Depends
from .auth.permissions import Permissions
from ..config import server
from ..service.grouping import group_records
from tracardi.service.storage.driver import storage
from typing import Optional
from tracardi.domain.report import Report


router = APIRouter(
    dependencies=[Depends(Permissions(roles=["admin", "developer"]))]
)


@router.get("/report/{id}", tags=["report"], include_in_schema=server.expose_gui_api)
async def get_report(id: str):
    """
    Returns report with given ID. Roles: admin, developer
    """
    result = await storage.driver.report.load(id)

    if result is None:
        raise HTTPException(status_code=404, detail=f"Report with ID {id} not found.")

    return result


@router.get("/reports", tags=["report"], include_in_schema=server.expose_gui_api)
async def load_grouped_reports(query: Optional[str] = None):
    """
    Returns list of reports according to given query, grouped by tag. Roles: admin, developer
    """
    result = await storage.driver.report.load_for_grouping(query)
    return group_records(result, None)


@router.post("/report", tags=["report"], include_in_schema=server.expose_gui_api)
async def add_report(report: Report):
    """
    Adds or edits report in the database. Roles: admin, developer
    """
    return await storage.driver.report.upsert(report)


@router.delete("/report/{id}", tags=["report"], include_in_schema=server.expose_gui_api)
async def delete_report(id: str):
    """
    Deletes report from the database
    """
    return await storage.driver.report.delete(id)
