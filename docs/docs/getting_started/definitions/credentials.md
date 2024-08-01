# Credentials

Credentials refer to the authentication details required to connect to external services or APIs. These
credentials are crucial for enabling Tracardi to interact with these services securely. Credentials are part of resource
configuration. Here are some key points about credentials in Tracardi:

1. **Types of Credentials**:
    - **API Keys**: Used for services like SendGrid, ClickSend, Airtable, etc. API keys are unique to each service and
      are required to authenticate API requests.
    - **Usernames and Passwords**: Used for services like Elasticsearch and Redis. These credentials authenticate the
      connection to the database or service.
    - **Tokens**: Used for services like Twilio, Telegram Bot API, and Matomo. Tokens act as passwords and are used to
      authenticate API requests.
    - **Client IDs and Secrets**: Used for services like Salesforce and AWS. These credentials are used in OAuth
      authentication flows and other secure API connections.

2. **Configuration and Setup**:
    - Credentials are typically configured through the Tracardi interface by filling out resource forms with the
      necessary authentication details.
    - Each external service has its own method for generating or retrieving these credentials, usually detailed in the
      service's documentation.

3. **Security**:
    - It is important to handle credentials carefully, ensuring they are not shared publicly or with unauthorized
      individuals. Tracardi database stores credentials so please make sure you do not expose it to public access.

4. **Examples of Credential Setup**:
    - **SendGrid**: To connect SendGrid to Tracardi, you need to generate an API key from the SendGrid dashboard and
      input it into the Tracardi resource form.
    - **ClickSend**: You need to log in to ClickSend, navigate to the API credentials section, and copy your username
      and API key into Tracardi.
    - **Airtable**: Find your Airtable API key in the account settings and input it into Tracardi.
    - **Twilio**: Retrieve your account SID and auth token from the Twilio dashboard and configure them in Tracardi.

5. **Caching**:
    - Credentials are subject to caching, meaning changes may not take effect immediately but after a set duration (
      typically 60 seconds).
