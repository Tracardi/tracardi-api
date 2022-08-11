from ..utils import Endpoint
from tracardi.domain.report import Report

endpoint = Endpoint()


def test_should_work():
    endpoint.post("/collect/page-view/@test-source", data={})  # TEST SOURCE HAS TO BE PRESENT AND ENABLED
    try:

        report = Report(
            id="@test-report",
            name="test-report",
            description="Here's report description.",
            index="event",
            query={"query": {"term": {"type": "{{type}}"}}},
            tags=["tag1", "tag2"]
        )
        result = endpoint.post("/report/test", data={"report": report.dict(), "params": {"type": "page-view"}})
        assert result.status_code == 200
        result = result.json()
        assert result["hits"]["hits"] != []
        assert all([record["_source"]["type"] == "page-view" for record in result["hits"]["hits"]])

        result = endpoint.post("/report", data=report.dict())
        assert result.status_code == 200

        result = endpoint.get("/report/@test-report")
        assert result.status_code == 200
        assert report == Report(**result.json())

        result = endpoint.post("/report/@test-report/run", data={"type": "page-view"})
        assert result.status_code == 200
        result = result.json()
        assert result["hits"]["hits"] != []
        assert all([record["_source"]["type"] == "page-view" for record in result["hits"]["hits"]])

        result = endpoint.get("/reports")
        assert result.status_code == 200
        result = result.json()
        assert result["total"] >= 1
        assert report.id in {data["id"] for data in result["grouped"]["tag1"]}
        assert report.id in {data["id"] for data in result["grouped"]["tag2"]}

    finally:
        result = endpoint.delete("/report/@test-report")
        assert result.status_code == 200
