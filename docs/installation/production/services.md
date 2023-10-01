# Production services

This is the list services/dockers for production ready Tracardi installation.

Service    | Description
-----| -------------
GUI    | Not exposed to the internet, VPN only.
Collector API    | Exposed to the internet, limited to collecting data only, no GUI.
Production API    | Not exposed to the internet, VPN only, access to production data.
Staging API    | Not exposed to the internet, VPN only, access to test data.
Scheduler    | Service for rescheduling delayed events.
Scheduler Worker    | Service responsible for executing delayed events.
Segmentation Job    | Periodically runs and checks for profiles to run through segmentation process.
Segmentation Worker    | Runs defined segmentation process.
Trigger Worker    | Runs when a profile is segmented and a workflow should be triggered.
Update and Migration    | Set of workers for system migration and data import.
Bridges    | Services for collecting data from different channels, bridges transportation protocol to Tracardi event source.

## Collector API

The Collector API is the API that should be exposed to the internet. It has a limited API function that is designed
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

## Staging API

The Staging API is the API that should not be exposed to the internet. It has API functions that provide access to test
data. Access to this server should be limited to people working on data orchestration.

### Access:

Access to the Staging API is restricted, and only personnel working on data orchestration should have access to this
server.

### Limitations:

This API is not exposed to the internet, and access to test data is restricted to personnel working on data
orchestration.

## Scheduler

The Scheduler is a service that reschedules the execution of delayed events. A delayed event occurs when a workflow
pauses and resumes after some time.

### Functionality:

The Scheduler is responsible for rescheduling the execution of delayed events in the system.

## Scheduler Worker

The Scheduler Worker is a service that is responsible for executing the delayed events. A delayed event occurs when a
workflow pauses and resumes after some time.

### Functionality:

The Scheduler Worker is responsible for executing the delayed events in the system.

## Segmentation Job

The Segmentation Job is a job that runs periodically and checks if some profiles should be run through a segmentation
process.

### Functionality:

The Segmentation Job runs periodically and checks for profiles that need to be run through the segmentation process.

## Segmentation Worker

The Segmentation Worker runs a defined segmentation process.

### Functionality:

The Segmentation Worker is responsible for running the defined segmentation process in the system.

## Trigger Worker

The Trigger Worker runs every time a profile is added to the segment and there is a defined workflow that should be triggered.

## Update and Migration

The Update and Migration is a set of workers responsible for system migration, data import, etc.

### Functionality:

The Update and Migration workers are responsible for various tasks such as system migration and data import.

## Bridges

The Bridges are services responsible for collecting data from different channels. They bridge the defined transportation
protocol to tracardi event source.

### Functionality:

The Bridges collect data from different channels and bridge the transportation protocol to the tracardi event source.