# What is merging strategy?

The merging strategy in Tracardi is the method or algorithm used for combining different profiles or events to form a
single cohesive profile. It is one of the predefined methods that the system will use in case there is conflicting data
in the set of profiles that need to be merged into a single profile. An example of a strategy is an algorithm that
prioritizes the last update made to a profile, regardless of the channel from which the data was collected.

## Example of Merging Strategy

One of the strategies is Last Profile Update Wins.This strategy ensures that the most recent information is retained when
merging profiles. It prioritizes the last update
made to a profile, regardless of the channel that the data was collected from. This approach is useful when you want to
ensure that the most current data is always reflected in the unified profile.

### Example Scenario

Consider three profiles with the following attributes:

- **Profile A**:
    - Name: John Doe
    - Email: john.doe@example.com
    - Last Profile Updated: 2024-01-01

- **Profile B**:
    - Name: Jonathan Doe
    - Email: jon.doe@example.com
    - Last Profile Updated: 2024-02-01

- **Profile C**:
    - Name: John Doe
    - Email: johnny.doe@example.com
    - Last Profile Updated: 2024-03-01

Using the Last Profile Update Wins Strategy:

1. **Identify Profiles to Merge**: Profiles A, B, and C.
2. **Compare Timestamps**:
    - Profile A: 2024-01-01
    - Profile B: 2024-02-01
    - Profile C: 2024-03-01
3. **Prioritize Recent Data**:
    - Name: John Doe (Profile C)
    - Email: johnny.doe@example.com (Profile C)
4. **Merge Data**:
    - Name: John Doe
    - Email: johnny.doe@example.com
5. **Update Unified Profile**:
    - The unified profile will now have the name "John Doe" and the email "johnny.doe@example.com," reflecting the most
      recent updates.

By following this strategy, Tracardi ensures that the most up-to-date information is always present in the unified
profile, providing a reliable and current view of the user.