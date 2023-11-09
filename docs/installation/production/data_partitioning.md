# Tracardi Data Partitioning Guide

## Overview

Data partitioning is a critical strategy for managing large datasets. It involves dividing a database into distinct,
independent parts to improve manageability, performance, and availability. Tracardi utilizes this technique by
segmenting indices that contain substantial amounts of data into separate time-based indices.

## Benefits of Data Partitioning with Tracardi

Partitioning in Tracardi allows for:

- **Efficient Data Management**: Simplifies data operations, including maintenance and deletion.
- **Scalability**: Supports growing data volumes by distributing them across multiple indices.
- **Cost Optimization**: Old data can be moved to cost-effective storage solutions.

## Time-based Partitioning in Tracardi

Tracardi implements time-based partitioning for the following indices:

- **Events**
- **Profiles**
- **Sessions**
- **Logs**

Each of these indices can be subdivided into different time frames, such as:

- **Year**: Groups all data collected within a single year into one index.
- **Quarter**: Segregates data into indices for each quarter within a year.
- **Month**: Divides data monthly, creating a separate index for each month.
- **Day**: Creates daily indices for a more granular approach to data segmentation.

## Setting Up Partitioning

Partitioning is configured during the initial system setup through environmental variables and remains constant
throughout the lifecycle of the system. Below are the default values for each partitioning strategy:

1. `EVENT_PARTITIONING`
    - **Description**: This environment variable is used to determine the partitioning interval for event data.
    - **Default Value**: `'month'` - If not set, events will be partitioned monthly.

2. `PROFILE_PARTITIONING`
    - **Description**: This variable sets the partitioning frequency for user profiles.
    - **Default Value**: `'quarter'` - User profiles are partitioned quarterly by default.

3. `SESSION_PARTITIONING`
    - **Description**: This environment variable dictates the partitioning interval for session data.
    - **Default Value**: `'quarter'` - Sessions will be partitioned every quarter if no other value is provided.

4. `ENTITY_PARTITIONING`
    - **Description**: It configures the partitioning strategy for entities.
    - **Default Value**: `'quarter'` - Entities are set to be partitioned quarterly.

5. `ITEM_PARTITIONING`
    - **Description**: This environment variable specifies the partitioning schedule for items.
    - **Default Value**: `'year'` - Items are partitioned annually.

6. `LOG_PARTITIONING`
    - **Description**: Determines how log data is partitioned.
    - **Default Value**: `'month'` - Logs are partitioned on a monthly basis.

7. `DISPATCH_LOG_PARTITIONING`
    - **Description**: Configures the partitioning of dispatch logs, which likely refer to logs that record the
      dispatching of events or profiles.
    - **Default Value**: `'month'` - Dispatch logs follow a monthly partitioning strategy.

8. `CONSOLE_LOG_PARTITIONING`
    - **Description**: Sets the partitioning interval for console logs, possibly related to logs generated from a
      workflow operations.
    - **Default Value**: `'month'` - Console logs are partitioned monthly.

9. `USER_LOG_PARTITIONING`
    - **Description**: This variable is for partitioning logs related to user activities.
    - **Default Value**: `'year'` - User activity logs are partitioned yearly.

These environment variables are designed to control the granularity of data partitioning in an application, with default
values providing a fallback in case specific settings are not provided. The partitioning strategy can impact the
performance and manageability of data, especially in systems that handle large volumes or require efficient querying
capabilities.

These environment variables control the time frame at which new indices are created and subsequently how the data is
partitioned.

## Considerations for Data Volume

The frequency of data partitioning should correlate with the volume of data being processed:

- **Higher Volumes**: For larger datasets, it is recommended to partition more frequently to maintain optimal
  performance and manageability.
- **Lower Volumes**: For smaller datasets, less frequent partitioning may be adequate and more cost-effective.

Remember, once set, the partitioning intervals cannot be altered without reconfiguring and redeploying the system.

