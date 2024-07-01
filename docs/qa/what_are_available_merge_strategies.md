# What are available merge strategies?

Below is a table that describes all available merge strategies in Tracardi as of version 0.9.0.7:

| Strategy ID                       | Name                                            | Description                                                                                                          
|-----------------------------------|-------------------------------------------------|----------------------------------------------------------------------------------------------------------------------|
| `LAST_UPDATE`                     | Last updated value                              | This merge strategy uses the update date of a field to find the most recent value that will prevail.                 |
| `FIRST_UPDATE`                    | First inserted value                            | This merge strategy uses the update date of a fieldto find the first inserted value that will prevail.               |
| `MIN`                             | Minimal value                                   | This merge strategy will select the minimal value as the merged value.                                               |
| `MAX`                             | Maximal value                                   | This merge strategy will select the maximal value as the merged value.                                               |
| `SUM`                             | Sum of values                                   | This merge strategy will sum all values and return it as the merged value.                                           |
| `AVG`                             | Average of values                               | This merge strategy will average all values and return it as the merged value.                                       |
| `LAST_DATETIME`                   | Last date                                       | This merge strategy works only on date values and will select the last date as the merged value.                     |
| `FIRST_DATETIME`                  | First date                                      | This merge strategy works only on date values and will select the first date as the merged value.                    |
| `ALWAYS_TRUE`                     | Always TRUE                                     | This merge strategy always returns TRUE as the merged value.                                                         |
| `ALWAYS_FALSE`                    | Always FALSE                                    | This merge strategy always returns FALSE as the merged value.                                                        |
| `AND`                             | AND Operator                                    | This merge strategy will use the AND operator on all boolean values and return it as the merged value.               |
| `OR`                              | OR Operator                                     | This merge strategy will use the OR operator on all boolean values and return it as the merged value.                |
| `MERGE_LISTS`                     | Merge Values From Lists                         | This merge strategy is used on lists and will concatenate all values and return them as the merged value.            |
| `MERGE_LISTS_DISTINCT`            | Merge Unique Values From Lists                  | This merge strategy is used on lists and will concatenate all values and return unique values as the merged value.   |
| `MERGE_LISTS_AND_VALUES_DISTINCT` | Merge Values and List of Values to Unique Lists | This merge strategy is used on lists and values and will concatenate all values and return unique values as a list.  |
| `MERGE_LISTS_AND_VALUES`          | Merge Values and List of Values to Unique Lists | This merge strategy is used on lists and values and will concatenate all values and return all values as a list.     |
| `CONCAT_VALUES_TO_LIST`           | Concatenates Values To A List                   | This merge strategy concatenates all values and returns unique values as a list.                                     |
| `CONCAT_DISTINCT_VALUES_TO_LIST`  | Concatenates Distinct Values To A List          | This merge strategy concatenates all values and returns unique values as a list.                                     |
| `FIRST_PROFILE_INSERT_TIME`       | First Profile Insert Time                       | This merge strategy will select the first inserted profile and get the value for the merged field from this profile. |
| `FIRST_PROFILE_UPDATE_TIME`       | First Profile Update Time                       | This merge strategy will select the first updated profile and get the value for the merged field from this profile.  |
| `FIRST_PROFILE_CREATE_TIME`       | First Profile Create Time                       | This merge strategy will select the first created profile and get the value for the merged field from this profile.  |
| `LAST_PROFILE_CREATE_TIME`        | Last Profile Create Time                        | This merge strategy will select the last created profile and get the value for the merged field from this profile.   |
| `LAST_PROFILE_UPDATE_TIME`        | Last Profile Update Time                        | This merge strategy will select the last updated profile and get the value for the merged field from this profile.   |
| `LAST_PROFILE_INSERT_TIME`        | Last Profile Insert Time                        | This merge strategy will select the last inserted profile and get the value for the merged field from this profile.  |
| `FIRST_ITEM`                      | No Merging                                      | This merge strategy will not merge anything.                                                                         |

## Examples

### Last Update Strategy

The Last Update Strategy prioritizes the most recent information when merging profiles. It uses the update date of a
field to select the latest value among conflicting data.

**Example Scenario**:

Consider two profiles with conflicting email information:

- **Profile A**:
    - Email: john.doe@example.com
    - Field was Updated: 2024-01-01

- **Profile B**:
    - Email: johnny.doe@example.com
    - Field was Updated: 2024-03-01

Using the Last Update Strategy:

1. **Compare Timestamps of Fields**:
    - Profile A: 2024-01-01
    - Profile B: 2024-03-01
2. **Select Most Recent Data**:
    - Email: johnny.doe@example.com (Profile B)

The unified profile will have the email "johnny.doe@example.com" as it is the most recently updated value.

### Last Profile Update Time Strategy

The Last Profile Update Time Strategy selects the value from the profile that was last updated. This is particularly
useful when merging data from profiles that have been updated at different times.

**Example Scenario**:

Consider three profiles with different names and update times:

- **Profile A**:
    - Name: John Doe
    - Profile Update Time: 2024-01-10

- **Profile B**:
    - Name: Jonathan Doe
    - Profile Update Time: 2024-02-15

- **Profile C**:
    - Name: Johnny Doe
    - Profile Update Time: 2024-03-05

Using the Last Profile Update Time Strategy:

1. **Compare Profile Update Times**:
    - Profile A: 2024-01-10
    - Profile B: 2024-02-15
    - Profile C: 2024-03-05
2. **Select Most Recently Updated Profile**:
    - Name: Johnny Doe (Profile C)

The unified profile will have the name "Johnny Doe" as it is from the profile that was last updated.

### Last DateTime Strategy

The Last DateTime Strategy is used for date values and selects the most recent date.

**Example Scenario**:

Consider three profiles with different last login dates:

- **Profile A**:
    - Last Login: 2024-01-01

- **Profile B**:
    - Last Login: 2024-02-01

- **Profile C**:
    - Last Login: 2024-03-01

Using the Last DateTime Strategy:

1. **Compare Dates**:
    - Profile A: 2024-01-01
    - Profile B: 2024-02-01
    - Profile C: 2024-03-01
2. **Select Most Recent Date**:
    - Last Login: 2024-03-01 (Profile C)

The unified profile will have the last login date "2024-03-01" as it is the most recent date.