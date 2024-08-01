# Profile

A profile in Tracardi represents an aggregated and comprehensive set of data about a customer, built dynamically as
events are processed by the system. Profile is referenced in [sessions](session.md), and [events](event.md). It captures
all relevant information and interactions pertaining to a user/customer, allowing for personalized and context-aware
actions within Tracardi workflows.

## Key Components of a Profile

1. **Profile ID**:
    - A unique identifier (usually a UUID) that distinguishes the profile from other profiles.

2. **Profile IDS**:
    - A number unique identifier (usually a UUID) that identifies the profile on different devices. Profile can be
      identified by many IDS.

2. **Data and Custom Traits**:
    - Key-value pairs that store various attributes of the profile. These include demographic information, preferences,
      behavioral data, and more (e.g., name, email, age, location, purchase history).

3. **Metadata**:
    - Additional context about the profile, such as creation and update timestamps, source information, and tags for
      categorization.

4. **Consents**:
    - Data capturing the user’s permissions and agreements regarding data usage, ensuring compliance with privacy
      regulations.

