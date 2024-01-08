# How data is collected and what stages there are before the event is saved.

To understand the journey of an event in Tracardi before it gets saved, let's break down each step you've mentioned:

1. **Data Validation**:
    - Purpose: To ensure that the incoming event data conforms to predefined standards and formats.
    - How It Works: When an event is received, Tracardi checks it against a set of validation rules defined as
      JSONSchema validation.

2. **Event Reshaping**:
    - Purpose: To transform or reformat the event data into a structure that is consistent and suitable for further
      processing and storage.
    - How It Works: This involves modifying the event data, if necessary, to align with the expected schema or format.
      It might include operations like renaming fields, or restructuring nested data.

3. **Event Mapping**:
    - Purpose: To ensure that the data from the event is correctly indexed.
    - How It Works: This step involves mapping the event data to the event traits. It ensures
      that each piece of data is stored in the right place. Each part of event has different properties. For example
      traits are indexed while properties are not. Please search the documentation for more information.

4. **Profile Identification Checkpoint**:
    - Purpose: To determine if the event data can be linked to/merged with an existing customer profile.
    - How It Works: Tracardi examines the event to see if it contains identifiers that can link it to an existing
      customer profile (like email, customer ID, etc.). If such identifiers are found, Tracardi associates the event
      with the corresponding profile.

5. **Event to Profile Mapping**:
    - Purpose: To transfer relevant data from the event to the customer's profile.
    - How It Works: Once an event is identified as belonging to a specific customer, certain data from the event may be
      used to update or augment the customer’s profile. This could include updating contact information, adding new
      preferences, tracking recent interactions, etc.

