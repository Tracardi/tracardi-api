# Twitter

Twitter is a free social networking site where users broadcast short posts known as tweets. These tweets can contain
text, videos, photos or links

## Resource configuration and set-up

To create your twitter application please follow these steps.

1. Go to  https://apps.twitter.com/ sing in your Twitter account and then click on the __"Create new app"__ button.
2. Choose __App Environment__, then type your application name, Click __Next__
3. Now click __"Go to dashboard"__ button in the bottom right corner.

## Permissions

Now you have to change your access level from Essential to Elevated, to do this you have to go through a few steps.

1. Go to https://developer.twitter.com/en/portal/products/elevated and change your access to elevated, then click __"
   Apply"__.
2. Now you will need to provide information why you do you need elevated access.

If you get Elevated access level then you have to change User authentication settings

1. On the list in left side expand __Projects and Apps__ and click __your project name__. The same name you set in the
   previous steps.
2. Now in the bottom of page you can see __"User authentication settings"__ section, click on __"Set up"__ button in
   this section.
3. Change App permission to __"Read and write"__, choose type of your app (most probably __Web App, Automated App or
   Bot__)
4. Fill App info with the following information:
    1. Callback URI - the webhook from the Tracardi source. Create a source that will receive events from Twitter and
       copy the source webhook to the form.
    2. Website URL - you website URL
    3. Organization name - you business name, or website name.
5. Confirm that you want to change you permissions.
6. Copy Client ID and Client Secret in case you need them.

## Generate API keys

If the previous steps have been completed now you can generate your API keys.

1. Expand __Projects and Apps__ and click __your app name__.
2. Now select __"Keys and tokens"__ in the tabs (right after the app title).
3. Click __Generate__ button in the __Consumer Keys__ section. Button next to __API Key and Secret__.
4. Copy the __API Key and API Key Secret__ to the Tracardi form
5. Click __Generate__ button in the __Authentication Tokens__ section. Button next to __Access Token and Secret__.
6. Copy the __Access Token and Access Token Secret__ to the Tracardi form