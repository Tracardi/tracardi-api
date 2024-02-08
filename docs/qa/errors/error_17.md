# In version 0.8.2.1 I got this error what should I do

```2024-02-08 11:51:05,011: ERROR: Update of index prod-0820.ffe49.tracardi-log-2024-2 mapping failed with error RequestError(400, 'illegal_argument_exception', {'error': {'root_cause': [{'type': 'illegal_argument_exception', 'reason': 'mapper [level] cannot be changed from type [text] to [keyword]'}], 'type': 'illegal_argument_exception', 'reason': 'mapper [level] cannot be changed from type [text] to [keyword]'}, 'status': 400}): (tracardi.service.setup.setup_indices:log_handler.py:51)```

This error typically occurs when the Elasticsearch (ES) log index is automatically created without a pre-existing
template for that index. Although Tracardi aims to avoid this issue, it may still arise under certain circumstances,
such as after system installation followed by an ES cluster failure and subsequent restart with a new instance. To
resolve this problem, you should delete the affected log indexes (for instance, 0820.ffe49.tracardi-log-2024-2 and
prod-0820.ffe49.tracardi-log-2024-2) and then refresh your system console in the browser. This action will prompt a
reinstallation process that should correct the error.