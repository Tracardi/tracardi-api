Mautic is the open-source marketing automation platform. The software has all the essential features like lead
management, campaign management, contacts and emails and responsive email creation

# Resource configuration and set-up

To use this resource, you first need to enable Mautic API. Go to Mautic configuration,
then to `API Settings` and make sure that `API enabled?` option is set to `Yes`.

To connect to Mautic, three parameters are needed:

#### Public key and private key
Go to API Credentials on the right side menu. Select `OAuth 2` as a protocol,
name the credentials to recognize them later, and fill in Tracardi API URL as 
`Redirect URI`. This parameter is to specify all hosts (separated by commas), that
are going to connect to Mautic API. Public and private key should now be generated.

#### API URL
This is simply your Mautic API host.
