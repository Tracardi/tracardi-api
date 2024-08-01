GitHub is an internet hosting service for software development and version control using Git.

# Resource configuration and set-up

To add a GitHub resource, you need to add your PAT (personal access token).

1. __api_url__ - usually this does not need changing and can be left at the default value of https://api.github.com.
2. __personal_access_token__ - this is a personal access token linked to your GitHub account. Refer to the link below
   for how to generate a PAT.

# Getting the access token

1. In the upper-right corner of any page, click your profile photo, then click Settings.
2. In the left sidebar, click Developer settings.
3. In the left sidebar, under Personal access tokens, click Tokens (classic).
4. Select Generate new token, then click Generate new token (classic).
5. In the "Note" field, give your token a descriptive name.
6. To give your token an expiration, select Expiration, then choose a default option or click Custom to enter a date.
7. Select the scopes you'd like to grant this token. To use your token to access repositories from the command line,
   select repo. A token with no assigned scopes can only access public information. For more information, see "Scopes
   for OAuth apps." on Github Documentation.
8. Click Generate token.
9. Optionally, to copy the new token to your clipboard

For more details you can refer to the following help articles:

* [Github documentation on personal tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token)
