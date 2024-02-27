from typing import Callable

from tracardi.service.storage.mysql.utils.select_result import SelectResult


def get_result_dict(records: SelectResult, mapping, filter: Callable=None):
    if not records.exists():
        return {
            "total": 0,
            "result": []
        }

    result = list(records.map_to_objects(mapping, filter))

    return {
        "total": records.count(),
        "result": result
    }


def get_grouped_result(label: str, records: SelectResult, mapping):

    result = list(records.map_to_objects(mapping))
    if not result:
        return {
            "total": 0,
            "grouped": None
        }

    return {
        "total": records.count(),
        "grouped": {
            label: result
        }
    }
