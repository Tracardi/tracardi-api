HubSpot's integrated CRM platform contains the marketing, sales, service, operations, and website-building software you
need to grow your business.

# Resource configuration and set-up

To use Hubspot you will need an API Key from their dashboard.

To obtain AccessToken/API KEY:

1. Log in to Hubspot as regular user
2. Go to Settings (upper right corner - Gear icon)
3. Find "Account Setup" -> "Integrations" -> "Private Apps" and click it
4. Click "Create Private App"
5. Fill the name and description in "Basic Info" tab
6. Set the scope/permission for any actions you want to do (crm.objects.contacts, crm.objects.companies, etc) in "
   Scopes" tab. We suggest to select the following scopes for the Tracardi plugins to work. 
   ```
   crm.objects.companies.write, 
   crm.objects.companies.read, 
   crm.objects.contacts.write, 
   crm.schemas.contacts.read, 
   content
   ``` 
7. Click "Create app"
8. You should see and alert "You're about to create a new private app. This will generate an access token that can be
   used to view or update your HubSpot account data.". Click "Continue creating".
9. Click show token and Copy token
10. Paste token to Token field in Tracardi form
