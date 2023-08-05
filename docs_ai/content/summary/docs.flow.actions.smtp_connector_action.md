This plugin is designed to send emails using SMTP servers. It supports sending HTML messages and requires configuration.
The configuration includes the message to be sent, the recipient, the sender, the reply-to address, and the subject. The
message can be a Tracardi template, which allows for the merging of plain text or HTML with data from the profile,
event, or session. The node also requires access to a resource that configures the SMTP server credentials, which
includes the SMTP server, port, username, password, and timeout. The node does not process input payload and returns
true if the mail was sent or false if there was an error.