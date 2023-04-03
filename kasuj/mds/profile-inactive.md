# Event: Profile Inactive

This event should be used to indicate that a customer profile has been marked as inactive, meaning that the account is
no longer active or has been suspended. This could be due to a variety of reasons such as the customer closing their
account, failing to meet certain requirements, a violation of terms of service, or defined period of inactivity.

Example usage:

* A customer has failed to meet the requirements of a subscription service and their account has been marked as
  inactive.

## Expected properties.

!!! Tip

    All properties are optional. If any property is missing it will not be processed and no error will be reported.

| Name   | Expected type   | Example                                              |
|--------|-----------------|------------------------------------------------------|
| reason  | string          | "Failed to meet subscription requirements" |

## Auto indexing

Data will not be indexed.

## Copy event data to profile

When an event occurs, the data associated with it will be automatically duplicated in certain profile properties. You
can refer to the table below for the exact mapping of which fields will be copied.

| Profile field             | Value         | Action                |
|---------------------------|---------------|-----------------------|
| active                    |     False     | Set. |

    