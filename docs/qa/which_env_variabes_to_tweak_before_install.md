# Which environment variables should I set before production installation?

Sure, here is the list including the new environment variables that can not be changed later or will require significant effort after installation:

### Environment Variables

1. **EVENT_PARTITIONING**
    - **Explanation**: Specifies the partitioning strategy for event data. Determines how event data is organized over
      time.
    - **Default Value**: `quarter`

2. **PROFILE_PARTITIONING**
    - **Explanation**: Specifies the partitioning strategy for profile data. Determines how profile data is organized
      over time.
    - **Default Value**: `quarter`

3. **SESSION_PARTITIONING**
    - **Explanation**: Specifies the partitioning strategy for session data. Determines how session data is organized
      over time.
    - **Default Value**: `quarter`

4. **ENTITY_PARTITIONING**
    - **Explanation**: Specifies the partitioning strategy for entity data. Determines how entity data is organized over
      time.
    - **Default Value**: `quarter`

5. **ITEM_PARTITIONING**
    - **Explanation**: Specifies the partitioning strategy for item data. Determines how item data is organized over
      time.
    - **Default Value**: `year`

6. **LOG_PARTITIONING**
    - **Explanation**: Specifies the partitioning strategy for general logs. Determines how log data is organized over
      time.
    - **Default Value**: `month`

7. **DISPATCH_LOG_PARTITIONING**
    - **Explanation**: Specifies the partitioning strategy for dispatch logs. Determines how dispatch log data is
      organized over time.
    - **Default Value**: `month`

8. **CONSOLE_LOG_PARTITIONING**
    - **Explanation**: Specifies the partitioning strategy for console logs. Determines how console log data is
      organized over time.
    - **Default Value**: `month`

9. **USER_LOG_PARTITIONING**
    - **Explanation**: Specifies the partitioning strategy for user logs. Determines how user log data is organized over
      time.
    - **Default Value**: `year`

10. **FIELD_CHANGE_LOG_PARTITIONING**
    - **Explanation**: Specifies the partitioning strategy for field change logs. Determines how field change log data
      is organized over time.
    - **Default Value**: `month`

11. **AUTO_PROFILE_MERGING**
    - **Explanation**: Sets the secret key for hashing data during the automatic profile merging process. This is used
      to ensure secure merging of profiles.
    - **Default Value**: `s>a.d-kljsa87^5adh`

12. **INSTALLATION_TOKEN**
    - **Explanation**: Token used for the installation process. It is required for setting up and initializing Tracardi.
    - **Default Value**: `tracardi`

13. **ELASTIC_INDEX_REPLICAS**
    - **Explanation**: Specifies the number of replica shards for Elasticsearch indices. Determines the number of copies
      of each shard.
    - **Default Value**: `1`

14. **ELASTIC_INDEX_SHARDS**
    - **Explanation**: Specifies the number of primary shards for Elasticsearch indices. Determines how the index is
      divided.
    - **Default Value**: `3`

15. **ELASTIC_CONF_INDEX_SHARDS**
    - **Explanation**: Specifies the number of primary shards for Elasticsearch configuration indices. Used for specific
      configurations of the Elasticsearch setup.
    - **Default Value**: `1`

