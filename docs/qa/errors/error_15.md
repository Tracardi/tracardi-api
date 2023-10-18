# I have this error: tracardi.exceptions.exception.StorageException: NotFoundError(404, 'index_not_found_exception', 'no such index [01506.tracardi-event-validation]', 01506.tracardi-event-validation, index_or_alias)

This suggests that the system is either not installed or configured as a multi-tenant instance without the MULTI_TENANT
setting set to 'yes.' Please refer to the documentation to learn how to enable multi-tenancy.