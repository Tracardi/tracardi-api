from fastapi import APIRouter
from fastapi import HTTPException, Depends
from .auth.permissions import Permissions
from tracardi.config import tracardi
from ..service.grouping import group_records
from tracardi.service.storage.driver.elastic import report as report_db
from typing import Optional
from tracardi.domain.report import Report
from app.api.domain.report_test_payload import ReportTestPayload
from tracardi.service.report_manager import ReportManager


router = APIRouter(
    dependencies=[Depends(Permissions(roles=["admin", "developer", "marketer"]))]
)


@router.get("/reports/entities", tags=["report"], include_in_schema=tracardi.expose_gui_api)
async def load_report_entities():
    """
    Returns list of reports as named entities. Roles: admin, developer, marketer
    """
    return {"result": [dict(id=report.id, name=report.name) for report in await report_db.load_all()]}


@router.get("/report/{id}", tags=["report"], include_in_schema=tracardi.expose_gui_api)
async def get_report(id: str):
    """
    Returns report with given ID. Roles: admin, developer, marketer
    """
    result = await report_db.load(id)

    if result is None:
        raise HTTPException(status_code=404, detail=f"Report with ID {id} not found.")

    return result


@router.get("/reports", tags=["report"], include_in_schema=tracardi.expose_gui_api)
async def load_grouped_reports(query: Optional[str] = None):
    """
    Returns list of reports according to given query, grouped by tag. Roles: admin, developer, marketer
    """
    result = await report_db.load_for_grouping(query)
    return group_records(result, None)


@router.post("/report", tags=["report"], include_in_schema=tracardi.expose_gui_api)
async def add_report(report: Report):
    """
    Adds or edits report in the database. Roles: admin, developer, marketer
    """
    result = await report_db.upsert(report)
    await report_db.refresh()
    return result


@router.delete("/report/{id}", tags=["report"], include_in_schema=tracardi.expose_gui_api)
async def delete_report(id: str):
    """
    Deletes report from the database
    """
    result = await report_db.delete(id)
    await report_db.refresh()
    return result


@router.post("/report/test", tags=["report"], include_in_schema=tracardi.expose_gui_api)
async def get_report_test(config: ReportTestPayload):
    manager = ReportManager(config.report)
    return await manager.get_report(config.params)


@router.post("/report/{id}/run", tags=["report"], include_in_schema=tracardi.expose_gui_api)
async def run_report(id: str, params: dict):
    manager = await ReportManager.build(id)
    return await manager.get_report(params)
