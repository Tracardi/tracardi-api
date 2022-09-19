CiviCRM is a web-based suite of internationalized open-source software for constituency relationship management. CiviCRM
is designed to manage information about an organization's donors, members, event registrants, subscribers,
grant-application seekers and funders, and case contacts. Volunteers, activists, and voters - as well as more general
sorts of business contacts such as employees, clients, or vendors.

# Resource configuration and set-up

To set up this resource, API key, Site key and API URL are needed.

### API Key

API keys are unique to CiviCRM contacts. You should add the API key to the contact,
and grant appropriate permissions to this contact. You can do it by API explorer, or
editing/adding a contact in any other way.

### Site key

Site key can be found in __civicrm.settings.php__ file on the server. Its location
can vary between CMSs and versions. The file should contain something like:

```php
if (!defined('CIVICRM_SITE_KEY')) {
  define( 'CIVICRM_SITE_KEY', 'qwednKcpN93x0mvv');
}
```

In this case, the Site key is __qwednKcpN93x0mvv__.

### API URL

Here provide the host of your CiviCRM instance, extended by __/sites/all/modules/civicrm/extern/rest.php__, or
the location of __rest.php__ file if it has been moved.