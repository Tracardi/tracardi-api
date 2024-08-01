# Workflow Trigger

A workflow trigger is a condition that initiates the execution of a workflow. Triggers are crucial
for defining when and how workflows should start, allowing for automated responses to specific events or changes within
the system.

## Key Aspects of Workflow Triggers:

1. **Triggers are Event-Based**:
    - Workflows are triggered in response to specific events occurring within the system. For example, a
      purchase event, a user logging in, or a page view can all serve as event-based triggers.

## Examples of Workflow Triggers:

1. **User Registration Event**:
    - **Trigger**: A new user registers on the website.
    - **Workflow**: Sends a welcome email, updates the user profile with registration details, and adds the user to a
      new user segment.

2. **Abandoned Cart Event**:
    - **Trigger**: A user adds items to their cart but does not complete the purchase within a specified timeframe.
    - **Workflow**: Sends a reminder email to the user, offers a discount, and updates the user profile with the
      abandoned cart information.

3. **Profile Update Condition**:
    - **Trigger**: A user's profile is updated with a new email preference.
    - **Workflow**: Adjusts the email marketing preferences in the user's profile, ensuring future emails match the
      user's new preferences.

4. **Daily Data Processing**:
    - **Trigger**: Scheduled to run daily at 2 AM.
    - **Workflow**: Aggregates daily user activity data, updates analytics dashboards, and archives old data.

## Setting Up Workflow Triggers

Workflow triggers are configured within the Tracardi Workflow Editor. Here’s how to set them up:

1. **Select Trigger Type**:
    - Choose between event-based, condition-based, or scheduled triggers based on the desired initiation criteria for
      the workflow.

2. **Define Trigger Criteria**:
    - Specify the event type (e.g., purchase, login, page view).
    - Specify the event source
    - Define what consents must be granted to run the workflow
    - Specify the workflow

3. **Configure Workflow Actions**:
    - Design the workflow by adding nodes and defining actions that should be performed when the trigger activates the
      workflow.

4. **Save and Activate**:
    - Save the workflow configuration and activate it to start listening for the defined triggers.
