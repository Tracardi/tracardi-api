from tracardi.domain.storage_record import StorageRecords, StorageRecord, RecordMetadata


def test_should_assign_and_read_values():
    records = StorageRecords.build_from_elastic({
        "took": 5,
        "timed_out": False,
        "_shards": {
            "total": 1,
            "successful": 1,
            "skipped": 0,
            "failed": 0
        },
        "hits": {
            "total": {
                "value": 20,
                "relation": "eq"
            },
            "max_score": 1.3862942,
            "hits": [
                {
                    "_index": "my-index-000001",
                    "_id": "0",
                    "_score": 1.3862942,
                    "_source": {
                        "@timestamp": "2099-11-15T14:12:12",
                        "http": {
                            "request": {
                                "method": "get"
                            },
                            "response": {
                                "status_code": 200,
                                "bytes": 1070000
                            },
                            "version": "1.1"
                        },
                        "source": {
                            "ip": "127.0.0.1"
                        },
                        "message": "GET /search HTTP/1.1 200 1070000",
                        "user": {
                            "id": "kimchy"
                        }
                    }
                }
            ]
        }
    })

    assert isinstance(records, dict)
    first_record = records.first()

    assert isinstance(first_record, StorageRecord)
    assert first_record.get_metadata().index == "my-index-000001"
    assert first_record.get_metadata().id == "0"
    assert first_record['id'] == "0"
    assert first_record['@timestamp'] == "2099-11-15T14:12:12"
    assert first_record['source']['ip'] == "127.0.0.1"
    assert first_record['message'] == "GET /search HTTP/1.1 200 1070000"

    assert records.dict()['total'] == 20
    assert len(records) == 1
    assert len(records.dict()['result']) == 1

    records.transform_hits(lambda record: {"replaced": 1})

    list_of_records = list(records)
    assert list_of_records[0] == {'replaced': 1, 'id': '0'}
    assert list_of_records[0].get_metadata().index == "my-index-000001"


def test_should_handle_empty_data():
    records = StorageRecords.build_from_elastic()
    assert isinstance(records, dict)
    list_of_records = list(records)
    assert list_of_records == []
    assert records.dict()['total'] == 0
    assert records.dict()['result'] == []


def test_should_slice_records():
    records = StorageRecords.build_from_elastic({
        "took": 5,
        "timed_out": False,
        "_shards": {
            "total": 1,
            "successful": 1,
            "skipped": 0,
            "failed": 0
        },
        "hits": {
            "total": {
                "value": 20,
                "relation": "eq"
            },
            "max_score": 1.3862942,
            "hits": [
                {
                    "_index": "my-index-000001",
                    "_id": "0",
                    "_score": 1.3862942,
                    "_source": {
                        "@timestamp": "2099-11-15T14:12:12",
                        "http": {
                            "request": {
                                "method": "get"
                            },
                            "response": {
                                "status_code": 200,
                                "bytes": 1070000
                            },
                            "version": "1.1"
                        },
                        "source": {
                            "ip": "127.0.0.1"
                        },
                        "message": "GET /search HTTP/1.1 200 1070000",
                        "user": {
                            "id": "kimchy"
                        }
                    }
                },
                {
                    "_index": "my-index-000002",
                    "_id": "1",
                    "_score": 1.3862942,
                    "_source": {
                        "@timestamp": "2099-11-15T14:12:12",
                        "http": {
                            "request": {
                                "method": "get"
                            },
                            "response": {
                                "status_code": 200,
                                "bytes": 1070000
                            },
                            "version": "1.1"
                        },
                        "source": {
                            "ip": "127.0.0.1"
                        },
                        "message": "GET /search HTTP/1.1 200 1070000",
                        "user": {
                            "id": "kimchy"
                        }
                    }
                },
                {
                    "_index": "my-index-000003",
                    "_id": "2",
                    "_score": 1.3862942,
                    "_source": {
                        "@timestamp": "2099-11-15T14:12:12",
                        "http": {
                            "request": {
                                "method": "get"
                            },
                            "response": {
                                "status_code": 200,
                                "bytes": 1070000
                            },
                            "version": "1.1"
                        },
                        "source": {
                            "ip": "127.0.0.1"
                        },
                        "message": "GET /search HTTP/1.1 200 1070000",
                        "user": {
                            "id": "kimchy"
                        }
                    }
                }
            ]
        }
    })

    assert records[0]['id'] == '0'
    assert records[1]['id'] == '1'
    assert records[2]['id'] == '2'

    record = records[0]  # type: StorageRecord

    assert isinstance(record, StorageRecord)
    assert isinstance(record.get_metadata(), RecordMetadata)
    assert record.get_metadata().index == 'my-index-000001'

    assert [row['id'] for row in records[1:]] == ["1", "2"]
    assert [row['id'] for row in records[:1]] == ["0"]
    assert [row['id'] for row in records[0:2]] == ["0", "1"]

    for i, row in enumerate(records[0:2]):
        assert isinstance(row, StorageRecord)
        assert isinstance(row.get_metadata(), RecordMetadata)
        assert row.get_metadata().index == f'my-index-00000{i+1}'

