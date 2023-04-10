# Errors

## Response - 422 Unprocessed entity

This error occurs when the tracker payload is missing some data. Usually it will happen when you miss required field.

## Response - Unauthorized

This error occurs when the `source.id` that is sent with payload does not exist in Tracardi.

## Response - Headers

With response there is a `x-process-time` header thar returns how much time it took to process the request.