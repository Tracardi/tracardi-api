from tracardi.service.storage.mysql.utils.select_result import SelectResult


def get_result_dict(records: SelectResult, mapping):
    if not records.exists():
        return {
            "total": 0,
            "result": []
        }
    return {
        "total": records.count(),
        "result": list(records.map_to_objects(mapping))
    }


def get_grouped_result(label: str, records: SelectResult, mapping):
    return {
        "total": records.count(),
        "grouped": {
            label: list(records.map_to_objects(mapping))
        }
    }
