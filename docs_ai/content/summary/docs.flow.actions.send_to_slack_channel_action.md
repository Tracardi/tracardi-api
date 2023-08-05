This plugin allows users to post a text message to a defined channel on Slack. In order to use this plugin, users must
first create an app on Slack and install it into their workspace. They must also allow the app to write into channels
and copy the app's bot token. This token must then be pasted when creating a Tracardi resource. The plugin takes any
payload as input and returns a response from Slack API on port response or additional error info payload on port error
if an error occurs. The configuration of the plugin can be done either with a form or with advanced configuration. The
form requires users to select their Slack resource, type in the name of the channel they want their bot to post to, and
type in the message content. The advanced configuration requires users to provide the id and name of their Slack
resource, the name of the Slack channel, and the content of the message. Depending on the app's scopes, users may need
to add their app to the channel they want to post to.