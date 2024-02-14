from fastapi import APIRouter
from fastapi import HTTPException, Depends

from tracardi.service.storage.mysql.map_to_named_entity import map_to_named_entity
from tracardi.service.storage.mysql.mapping.report_mapping import map_to_report
from tracardi.service.storage.mysql.service.report_service import ReportService
from .auth.permissions import Permissions
from tracardi.config import tracardi
from ..service.grouping import get_grouped_result, get_result_dict
from typing import Optional
from tracardi.domain.report import Report
from app.api.domain.report_test_payload import ReportTestPayload
from tracardi.service.report_manager import ReportManager

router = APIRouter(
    dependencies=[Depends(Permissions(roles=["admin", "developer", "marketer"]))]
)


@router.get("/reports/entities", tags=["report"], include_in_schema=tracardi.expose_gui_api)
async def load_report_names():
    """
    Returns list of reports as named entities. Roles: admin, developer, marketer
    """

    rs = ReportService()
    records = await rs.load_all()
    return get_result_dict(records, map_to_named_entity)


@router.get("/report/{id}", tags=["report"], include_in_schema=tracardi.expose_gui_api)
async def get_report(id: str):
    """
    Returns report with given ID. Roles: admin, developer, marketer
    """
    rs = ReportService()
    record = await rs.load_by_id(id)
    if not record.exists():
        raise HTTPException(status_code=404, detail=f"Report with ID {id} not found.")

    return record.map_to_object(map_to_report)


@router.get("/reports", tags=["report"], include_in_schema=tracardi.expose_gui_api)
async def load_all(query: Optional[str] = None, limit: int = 200):
    """
    Returns list of reports according to given query, grouped by tag. Roles: admin, developer, marketer
    """

    rs = ReportService()
    records = await rs.load_all(search=query, limit=limit)

    return get_grouped_result("Reports", records, map_to_report)


@router.post("/report", tags=["report"], include_in_schema=tracardi.expose_gui_api)
async def add_report(report: Report):
    """
    Adds or edits report in the database. Roles: admin, developer, marketer
    """

    rs = ReportService()
    return await rs.insert(report)


@router.delete("/report/{id}", tags=["report"], include_in_schema=tracardi.expose_gui_api)
async def delete_report(id: str):
    """
    Deletes report from the database
    """
    rs = ReportService()
    return await rs.delete_by_id(id)


@router.post("/report/test", tags=["report"], include_in_schema=tracardi.expose_gui_api)
async def get_report_test(config: ReportTestPayload):
    manager = ReportManager(config.report)
    return await manager.get_report(config.params)


@router.post("/report/{id}/run", tags=["report"], include_in_schema=tracardi.expose_gui_api)
async def run_report(id: str, params: dict):
    manager = await ReportManager.build(id)
    return await manager.get_report(params)
