from ..utils import Endpoint
from tracardi.domain.report import Report

endpoint = Endpoint()


def test_should_work():

    event_source = dict(
        id="@test-source",
        type="rest",
        name="Test",
        timestamp="2022-01-07T16:18:09.278Z",
        enabled=True,
        returns_profile=True,
        config={}
    )

    response = endpoint.post('/event-source', data=event_source)
    assert response.status_code in [200]

    result = endpoint.post("/collect/report-test/@test-source", data={})
    assert result.status_code == 200
    try:

        report = Report(
            id="@test-report",
            name="test-report",
            description="Here's report description.",
            index="event",
            query={"query": {"term": {"type": "{{type}}"}}},
            tags=["tag1", "tag2"]
        )
        result = endpoint.post("/report/test", data={"report": report.dict(), "params": {"type": "report-test"}})
        assert result.status_code == 200
        result = result.json()

        assert result["result"] != []
        assert all([record["type"] == "report-test" for record in result["result"]])

        result = endpoint.post("/report", data=report.dict())
        assert result.status_code == 200

        result = endpoint.get("/report/@test-report")
        assert result.status_code == 200
        assert report == Report(**result.json())

        result = endpoint.post("/report/@test-report/run", data={"type": "report-test"})
        assert result.status_code == 200
        result = result.json()

        assert result["result"] != []
        assert all([record["type"] == "report-test" for record in result["result"]])

        result = endpoint.get("/reports")
        assert result.status_code == 200
        result = result.json()
        assert result["total"] >= 1
        assert report.id in {data["id"] for data in result["grouped"]["tag1"]}
        assert report.id in {data["id"] for data in result["grouped"]["tag2"]}

    finally:
        result = endpoint.delete("/report/@test-report")
        assert result.status_code == 200
        result = endpoint.delete("/event-source/@test-source")
        assert result.status_code == 200
