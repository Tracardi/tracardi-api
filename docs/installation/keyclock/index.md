# How to Set Up Tracardi with OAuth2

## Important Note

Please be aware that OAuth2 integration is a premium feature and is not included in the open-source version of Tracardi.

## Getting Started with Keycloak for Tracardi

Tracardi utilizes Keycloak as its identity management tool. To begin using Keycloak, execute the following Docker
command:

```bash
docker run -p 8080:8080 -e KEYCLOAK_USER=admin_user_placeholder -e KEYCLOAK_PASSWORD=admin_password_placeholder jboss/keycloak
```

In the command above, ensure that you replace `admin_user_placeholder` and `admin_password_placeholder` with your chosen
admin username and password, respectively.

## Important Warning

Be cautious of port conflicts; specifically, the default port `8080` may clash with Apache Pulsar's port. If you
encounter an error like:

```
Bind for 0.0.0.0:8080 failed: port is already allocated.
```

It indicates that the port is in use. To resolve this, modify the port mapping argument from `-p 8080:8080`
to `-p 8081:8080` in the Docker command. This change maps the container's internal port `8080` to the external
port `8081`, effectively avoiding the conflict.

## Configuring Keycloak

Once you've logged into Keycloak, you'll need to set up the realm and other necessary configurations for Tracardi
integration.

1. **Log in to Keycloak**: Access the Keycloak administration console and log in.

2. **Create a New Realm**: Hover over the 'Master' drop-down menu in the top left corner. This menu lists all created
   realms and includes the option to 'Add Realm'. Click this to create a new realm. On the 'Add Realm' page, specify the
   realm name and click 'Create'.

3. **Define Realm Settings**: After creating the realm, configure the settings such as tokens, sessions, and
   client registration.

4. **Create Clients**: Within your realm's configurations, proceed to create and set up clients that Tracardi will
   utilize for its authentication and authorization processes. Add a new client and set 'tracardi' as the ClientId.
   Client ID can be passed to the GUI as env variable KC_CLIENT_ID. Ensure you configure
   the `Valid Redirect URIs`, `Web Origins`, and `Backchannel Logout URL` are filled.

5. In a development the setting, looks like this:
    * `Valid Redirect URIs` - http://localhost:8787/*
    * `Web Origins` - http://localhost:8787 or you man allow all sites then set *
    * `Backchannel Logout URL` http://localhost:8787 or leave it empty

6. **Manage Users and Roles**: Set up users and define roles within the realm for access control.

7. **Configure Identity Providers**: If integrating with external identity providers, configure them in the realm
   settings.
