# Outbound traffic

Tracardi can connect to external services to query them for data. We call them outbound resources.
Information about resources is stored in Tracardi and can be referenced in Workflow. Workflow actions use them to
access external services.

## Credentials

Most of the resources need credentials that are used to connect to the resource. Credentials are attached to resource
and stored inside Tracardi.

!!! Info

    The part of the resource definition that contains sensitive data is encrypted. 

### Credentials caching

Credentials are subject to caching. That means that after they are changed you will not see the change immediately but
after a certain number of seconds. Usually 60 seconds. Search for `SOURCE_TTL` for more information on cache settings.