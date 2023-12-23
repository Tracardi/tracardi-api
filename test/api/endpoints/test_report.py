from uuid import uuid4

from tracardi.domain.event_source import EventSource
from .test_event_endpoint import _make_event
from test.utils import Endpoint
from tracardi.domain.report import Report

endpoint = Endpoint()


def test_should_work():

    event_source = EventSource(
        id="@test-source",
        bridge={"id": "1", "name": "API"},
        type="rest",
        name="Test",
        timestamp="2022-01-07T16:18:09.278Z",
        enabled=True,
        config={}
    )

    response = endpoint.post('/event-source', data=event_source.model_dump())
    assert response.status_code in [200]

    event_type = str(uuid4())
    session_id = str(uuid4())
    source_id = str(uuid4())
    response, _, events, profile_id = _make_event(event_type, session_id=session_id, source_id=source_id)

    try:

        report = Report(
            id="@test-report",
            name="test-report",
            description="Here's report description.",
            index="event",
            query={"query": {"term": {"type": "{{type}}"}}},
            tags=["tag1", "tag2"]
        )
        result = endpoint.post("/report/test", data={"report": report.model_dump(), "params": {"type": event_type}})
        assert result.status_code == 200
        result = result.json()

        assert result["result"] != []
        assert all([record["type"] == event_type for record in result["result"]])

        result = endpoint.post("/report", data=report.model_dump())
        assert result.status_code == 200

        result = endpoint.get("/report/@test-report")
        assert result.status_code == 200
        assert report == Report(**result.json())

        result = endpoint.post("/report/@test-report/run", data={"type": event_type})
        assert result.status_code == 200
        result = result.json()

        assert result["result"] != []
        assert all([record["type"] == event_type for record in result["result"]])

        result = endpoint.get("/reports")
        assert result.status_code == 200
        result = result.json()
        assert result["total"] >= 1
        assert report.id in {data["id"] for data in result["grouped"]["tag1"]}
        assert report.id in {data["id"] for data in result["grouped"]["tag2"]}

    finally:
        assert endpoint.delete("/report/@test-report").status_code == 200
        assert endpoint.delete(f'/event-source/{source_id}').status_code == 200
        assert endpoint.delete(f'/event/{events[0]}').status_code == 200
        assert endpoint.delete(f'/profile/{profile_id}').status_code == 200
        assert endpoint.delete(f'/session/{session_id}').status_code == 200

        assert endpoint.get('/events/refresh').status_code == 200
        assert endpoint.get('/profiles/refresh').status_code == 200
        assert endpoint.get('/event-sources/refresh').status_code == 200
        assert endpoint.get('/sessions/refresh').status_code == 200
