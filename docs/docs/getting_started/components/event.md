In Tracardi, events are records of actions or occurrences that take place at a specific point in time. They serve as the
primary mechanism for tracking and understanding user behavior on a website or application. Here’s a detailed overview
of events in Tracardi:

### Purpose of Events

- **Tracking User Behavior**: Events are used to monitor and record various user interactions and activities on a
  website or application.
- **Capturing Data**: Events can capture a wide range of data points, such as user actions, timestamps, and additional
  context-specific information.

### Examples of Events

- **Click Events**: Tracking when a user clicks on a link or button.
- **Login Events**: Recording when a user logs into an account.
- **Form Submissions**: Capturing data when a user submits a form.
- **Page Views**: Logging when a user views a specific page.
- **Purchase Orders**: Recording details of a purchase made by the user.

### Event Data

Events can carry various types of data depending on the interaction being tracked. This data can include:

- **User Information**: Details such as username or user ID.
- **Interaction Details**: Information about the action taken, such as the item purchased or the page viewed.
- **Contextual Data**: Additional information such as the device used, browser type, operating system, screen
  resolution, and other environmental details.

### Triggering Events

Events in Tracardi can be triggered in several ways:

- **JavaScript Execution**: Events can be triggered by executing JavaScript code on a webpage.
- **API Calls**: Events can be triggered by making API requests to the `/track` endpoint.

### Configurability

- **Customizable Event Types**: The types of events and the data they capture can be configured to meet specific
  tracking requirements.
- **Data Configuration**: The data sent with each event can be customized based on the type of event and the information
  needed.

### Event Processing

- **Storage**: Events can be stored within the Tracardi system for later analysis and reporting.
- **Workflow Integration**: Events can be passed to workflows for real-time processing and action. This allows for
  automated responses and further data manipulation based on the events.

### Types of Events

Tracardi supports four primary types of events:

- **Events with Profiles**: These events are associated with user profiles, providing a richer context by linking events
  to specific users.
- **[Events without Profiles](events/profile_less_events.md)**: These events are not linked to any user profile, useful for tracking anonymous or
  non-user-specific actions.
- **[Ephemeral events](events/ephemeral_events.md)**: Ephemeral events are temporary events that are processed without being permanently stored in the system
- **[System Events](events/system_events.md)**: System events in Tracardi are automatically generated events that record the internal workings of the system.

### Flexibility and Usage

Events provide a flexible and powerful way to track and respond to user interactions. They are fundamental to
understanding user behavior, personalizing user experiences, and driving data-driven decision-making within the Tracardi
system.

By leveraging events, Tracardi enables comprehensive monitoring, analysis, and automation of user interactions,
enhancing the ability to tailor experiences and optimize engagement strategies.