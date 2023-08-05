This plugin adds new contact to Elastic Email, based on provided data. It takes any payload as input and returns
response from Elastic Email API on port response, or optional error info on port error if one occurs. The plugin
configuration requires two form fields: Elastic Email resource and Email address. The Elastic Email resource should
contain the Elastic Email Client api key and the Email address should be the path to the email address you want the
status changed. The status should be the number for the status you want, with 2 being Unsubscribe. The JSON
configuration requires a resource with an id and name of the Elastic Email resource, the email path, and the status
number. This plugin is useful for adding new contacts to Elastic Email with the desired status.