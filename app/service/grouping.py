from collections import defaultdict
from app.service.grouper import search
from tracardi.domain.storage_record import StorageRecords
from typing import Optional

from tracardi.service.storage.mysql.utils.select_result import SelectResult


def group_records(
        result: StorageRecords,
        query: Optional[str] = None,
        group_by: Optional[str] = "tags",
        search_by: Optional[str] = "name",
        sort_by: Optional[str] = None
) -> dict:
    total = result.total

    # Filtering
    if query is not None and len(query) > 0:
        query = query.lower()
        if query:
            result = [r for r in result if query in r[search_by].lower() or (group_by is not None and search(query, r[group_by]))]

    # Grouping
    groups = defaultdict(list)
    for record in result:
        if group_by is not None and group_by in record:
            if isinstance(record[group_by], list):
                if len(record[group_by]) > 0:
                    for group in record[group_by]:
                        groups[group].append(record)
                else:
                    groups["General"].append(record)
            elif isinstance(record[group_by], str):
                groups[record[group_by]].append(record)
        else:
            groups["General"].append(record)

    # Sort
    if sort_by:
        groups = {k: sorted(v, key=lambda r: r[sort_by], reverse=False) for k, v in groups.items()}

    return {
        "total": total,
        "grouped": groups
    }


def group_mysql_records(
        result: list,
        query: Optional[str] = None,
        group_by: Optional[str] = "tags",
        search_by: Optional[str] = "name"
) -> dict:

    result = list(result)
    total = len(result)

    # Filtering
    if query is not None and len(query) > 0:
        query = query.lower()
        if query:
            result = [r for r in result if query in r[search_by].lower() or (group_by is not None and search(query, r[group_by]))]

    # Grouping
    groups = defaultdict(list)
    for record in result:
        if group_by is not None and group_by in record:
            if isinstance(record[group_by], list):
                if len(record[group_by]) > 0:
                    for group in record[group_by]:
                        groups[group].append(record)
                else:
                    groups["General"].append(record)
            elif isinstance(record[group_by], str):
                groups[record[group_by]].append(record)
        else:
            groups["General"].append(record)

    print(groups)

    # Sort
    groups = {k: sorted(v, key=lambda r: r.name, reverse=False) for k, v in groups.items()}

    return {
        "total": total,
        "grouped": groups
    }
