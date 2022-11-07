Mautic is the open-source marketing automation platform. The software has all the essential features like lead
management, campaign management, contacts and emails and responsive email creation

# Resource configuration and set-up

To use this resource, you first need to enable Mautic API. Go to Mautic configuration,
then to __API Settings__ and make sure that __API enabled?__ option is set to __Yes__.

To connect to Mautic, three parameters are needed:

## Public key and private key

Go to API Credentials on the right side menu. Select __OAuth 2__ as a protocol,
name the credentials to recognize them later, and fill in Tracardi API URL as
__Redirect URI__. This parameter is to specify all hosts (separated by commas), that
are going to connect to Mautic API. Public and private key should now be generated.

## API URL

This is your Mautic API host.

## Info

This resource can be used as destination
