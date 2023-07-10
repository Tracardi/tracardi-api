# YouTube widget

Shows a YouTube video widget.

## Description

The YouTube widget plugin allows you to embed a YouTube video widget in Tracardi. This plugin displays a YouTube video
based on the provided configuration. You can customize the display type, position, and other settings to suit your
needs.

This documentation is for version 0.8.1 of the YouTube widget plugin.

# Inputs and Outputs

This plugin has one input:

- **payload**: This port accepts a payload object.

This plugin has one output:

- **payload**: This port returns the given payload without any changes.

# Configuration

The YouTube widget plugin has the following configuration parameters:

- **YouTube ID**: Please provide the YouTube ID of the video you want to display.
- **Video Title**: Please provide the title of the video.
- **Popup lifetime**: Please provide the number of seconds for the popup to be displayed.
- **Display type**: Please select how you would like the video to be displayed. The available options are "Pop-up box"
  and "Modal window".
- **Horizontal position**: Select the horizontal position of the popup. The available options are "Left", "Center",
  and "Right".
- **Vertical position**: Select the vertical position of the popup. The available options are "Top" and "Bottom".

# Required resources

This plugin does not require any external resources to be configured.

# Errors

The YouTube widget plugin does not raise any specific errors. However, if there are any issues with loading or
displaying the YouTube video, they will be handled by the YouTube widget itself.

Note: The YouTube widget may display an error message if the provided YouTube ID is invalid or if there are any issues
with the YouTube API.