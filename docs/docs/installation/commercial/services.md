# Production services

This is the list services/dockers for production ready Tracardi installation.

Service    | Description                                                                                                               |
-----------|---------------------------------------------------------------------------------------------------------------------------|
Init | Installation script.                                                                                                      |
GUI        | Not exposed to the internet, VPN only.                                                                                    |
Public API | Exposed to the internet, limited to collecting data only, no GUI.                                                         |
Private API| Not exposed to the internet, VPN only, allows control of tracardi and its data.                                           |
Background Worker    | Runs defined background process.                                                                                          |
APM | Automatic profile merging worker.                                                                                         |
TMS | Tracardi Tenant Managemetn System. Needed for multitenant setups.                                                         |
Update and Migration    | Set of workers for system migration and data import.                                                                      |
Bridges    | Optional. Services for collecting data from different channels, bridges transportation protocol to Tracardi event source. | 

## Collector API

The Public API is the API that should be exposed to the internet. It has a limited API function that is designed
specifically for collecting data. No GUI-like operations are available.

### Access:

This API is accessible via the internet and can be utilized for collecting data.

### Limitations:

The Collector API does not have any GUI operations available, and its functionality is limited to collecting data only.

## Production API

The Production API is the API that should not be exposed to the internet. It has API functions that provide access to
production data. Only users who are authorized to see real data should have opened accounts on this instance.

### Access:

Access to the Production API is restricted and limited to authorized users only. Only users with opened accounts are
allowed to access the production data through this API.

### Limitations:

This API is not exposed to the internet, and access to production data is restricted to authorized users only.

## Private API

The Staging API is the API that should not be exposed to the internet. It has API functions that provide access to test
data. Access to this server should be limited to people working on data orchestration.

### Access:

Access to the Staging API is restricted, and only personnel working on data orchestration should have access to this
server.

### Limitations:

This API is not exposed to the internet, and access to test data is restricted to personnel working on data
orchestration.

## Background Worker

The Background Worker handles all background tasks, including triggering predefined workflows, storing events, and other similar jobs.

## Update and Migration

The Update and Migration is a set of workers responsible for system migration, data import, etc.

### Functionality:

The Update and Migration workers are responsible for various tasks such as system migration and data import.

## Bridges

This service is optional. The Bridges are services responsible for collecting data from different channels. They bridge the defined transportation
protocol to tracardi event source.

### Functionality:

The Bridges collect data from different channels and bridge the transportation protocol to the tracardi event source.