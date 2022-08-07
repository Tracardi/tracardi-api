from tracardi.domain.report import Report
from pydantic import BaseModel
from typing import Dict, Any


class ReportTestPayload(BaseModel):
    report: Report
    params: Dict[str, Any]
