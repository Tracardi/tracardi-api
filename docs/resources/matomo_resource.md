# Matomo Credentials

In order to connect to matomo you will need to provide an API address and a token

The token acts as your password and is used to authenticate in API requests. The token is secret and should be handled
very carefully: do not share it with anyone. Each Matomo user has a different token.

API address is the URL where the matomo API is installed.

# Where to get matomo token

You must be logged in to the Matomo server and do the following procedure.

## Matomo 4 and newer

To generate a token_auth follow these steps:

* Log in to Matomo
* Go to the Matomo Admin through the top menu (gear icon)
* Click on Personal -> Security
* In the bottom of the page click on "Create new token"
* Confirm your account password
* Enter the purpose for this plugin as a description
* Click on "Create new token"

You will now see the newly created token. Save it somewhere safe as you won’t be able to see it anymore once you leave
that screen. For example in a password manager. If you lose it, you will need to generate a new token.

We recommend you create a new token for every app or purpose. This way, you can easily delete or regenerate the token
for specific purposes and see which ones are still being used etc.

## Matomo 3 and older

You can find the token by logging in Matomo (Piwik), then click on Administration in the top menu, then click the link
“API” in the left menu.

The token_auth value can be re-generated on request by any user under Administration > Personal Settings.

# How do I find the Site ID

Matomo (Piwik) lets you measure several websites within one Matomo server. Each website added into Matomo has its very
own ID Site (or Website ID).

To find out the site ID value for a given website, you can follow these steps:

* Log into your Matomo.
* Go to Administration (click on the gear icon in the top right of the screen).
* Click on the Measurables(or Websites) > Manage page. You will find a list of all websites on this page.
* The website ID is on the left of the table listing all websites directly below the website name.

If you are using Matomo for WordPress, your Site ID should be 1 and you can double-check this ID in Matomo Analytics >
System Report > Matomo Blog idSite.
