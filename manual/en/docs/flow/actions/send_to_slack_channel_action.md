# Post to Slack channel plugin

This plugin posts a text message to defined channel on Slack.

## Requirements
This plugin requires adding an app to your Slack workspace:
- Add app to your workspace
- Allow this app to write into channels
- Copy this app's bot token
- Paste the token when creating Tracardi resource

For more detail, check Slack apps creating documentation.

## Inputs
This plugin takes any payload as input.

## Outputs
This plugin returns a response from Slack API on port **response** or empty payload
on port **error** if an error occurs.

## Configuration

#### With form
- Slack resource - Here select your Slack resource, containing your app's bot token.
- Slack channel - Here type in the name of the channel that you want your bot to post to.
- Message - Here type in the message content. You can use dot templates.

#### Advanced configuration
```json
{
  "source": {
    "id": "<id-of-your-slack-resource>",
    "name": "<name-of-your-slack-resource>"
  },
  "channel": "<name-of-slack-channel>",
  "message": "<content-of-your-message>"
}
```

## Warning
Depending on your app's scopes, you may need to add your app to the channel that
you want to post to.