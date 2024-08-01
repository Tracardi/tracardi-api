# How to start with Facebook integration

To get started with the Facebook SDK and create the necessary credentials like `YOUR_APP_ID`, `YOUR_APP_SECRET`,
and `YOUR_ACCESS_TOKEN`, you'll need to follow these steps:

1. **Create a Facebook Developer Account:**
    - If you don't already have one, you'll need to create a Facebook Developer account. Go to
      the [Facebook Developers website](https://developers.facebook.com/) and sign up.

2. **Create a New App:**
    - Once logged in, go to the 'My Apps' menu and select 'Create App'.
    - Choose the app type that best suits your needs (e.g., 'For Everything Else' if your app doesn't fit into the other
      categories).
    - Fill in the required information (like the name of your app, purpose: Business, connect business account if
      needed.) and click 'Create'.

3. **Get Your App ID and App Secret:**
    - After creating your app, you'll be redirected to the App Dashboard.
    - Here, you can find your 'App ID' and 'App Secret'. Go to `App Settings/Basic`. You will find the APP_ID and APP_SECRET. Keep these confidential.
    - You may need to click on 'Show' and enter your password to see the App Secret.

4. **Generate an Access Token:**
    - In the App Dashboard, look for the `App Settings/Advanced` section.
    - You can generate a User Access Token, which is tied to a specific user and allows the app to do things on behalf
      of that user.
    - For server-to-server calls, you might need an 'App Access Token' (which represents the app itself) or a 'Page
      Access Token' (for managing Facebook Pages).

7. **Source Audience ID:**
    - For the `source_audience_id`, you need an existing Custom Audience ID or any other valid source audience ID based
      on your requirements.

Ensure you adhere to Facebook's policies and guidelines while using their SDK and APIs, especially regarding user data
and privacy. If you're planning to use the app in a production environment, you might also need to go through Facebook's
App Review process.