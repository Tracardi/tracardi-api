# OpenReplay UX

The OpenReplay UX plugin injects the OpenReplay tracing script into a webpage. The tracing script allows you to capture and analyze user interactions and behaviors on your website. By integrating OpenReplay, you can gain valuable insights into how users navigate your site, identify potential issues, and optimize user experiences.

## Description

The OpenReplay UX plugin is designed to inject the OpenReplay tracing script into a webpage. This script is responsible for capturing and recording user interactions and behaviors on the website. The plugin appends the OpenReplay tracing script to the HTML of the webpage, enabling the collection of data related to user sessions.

When the plugin is executed, it injects the tracing script into the webpage using the provided OpenReplay project key. The project key is a unique identifier for your OpenReplay project. By configuring the plugin with your project key, the tracing script will send the captured data to your OpenReplay account for analysis.

Example output from the plugin:

```json
{
  "port": "response",
  "value": {
    // some data
  }
}
```

# Inputs and Outputs

The OpenReplay UX plugin has a single input and output port:

- Input: `payload` - This port accepts a payload object.
- Output: `response` - This port returns the input payload without any changes.

# Configuration

The OpenReplay UX plugin requires the following configuration:

- `Your Open Replay token`: This configuration field expects your OpenReplay project key. To obtain the project key, log in to openreplay.com, navigate to "Settings" > "Projects," and locate the Project Key associated with your project.

# JSON Configuration

Here is an example JSON configuration for the OpenReplay UX plugin:

```json
{
  "token": "your_open_replay_token"
}
```

# Required resources

This plugin does not require external resources to be configured.

# Errors

The following error may occur while using the OpenReplay UX plugin:

- **Project key can not be empty.**: This error occurs when the provided project key is empty. The project key is a required configuration parameter, and it cannot be left empty.