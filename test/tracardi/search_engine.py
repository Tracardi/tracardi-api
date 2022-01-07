import asyncio

from tracardi.domain.time_range_query import DatetimeRangePayload, DatePayload, DateDeltaPayload, DatetimeType
from tracardi.service.storage.elastic_storage import ElasticStorage
from tracardi.service.storage.persistence_service import SqlSearchQueryEngine, PersistenceService


async def main():
    query = DatetimeRangePayload(
        minDate=DatePayload(
            delta=DateDeltaPayload(value=-12, entity=DatetimeType.hour),
            absolute=None),
        maxDate=DatePayload(delta=None, absolute=None),
        where='',
        timeZone='Europe/Warsaw',
        start=0,
        limit=30,
        rand=0.4153204263631034
    )
    s = SqlSearchQueryEngine(PersistenceService(ElasticStorage('event')))
    result = await s.histogram(query)
    print(result)


asyncio.run(main())
