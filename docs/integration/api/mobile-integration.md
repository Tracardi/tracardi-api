# How to integrate Tracardi with mobile apps or external systems

Integrating Tracardi with mobile apps or external systems follows a similar process as integrating with a web page, with
the only difference being that Tracardi provides a JavaScript snippet that simplifies the integration. The JavaScript
snippet automates the process of calling the track endpoint and saving the Session ID and Profile ID in the browser.

However, when integrating with mobile apps or backend systems, the process needs to be done manually. It is crucial to
remember that both the Profile ID and Session ID must be saved on the customer's device or backend system for effective
tracking and personalization.

While it may be evident to save the Profile ID and Session ID when integrating with a mobile app, it may not be as
apparent when integrating with a PHP application or other server-side applications. In such cases, it is necessary to
set a PHPSESSIONID or other relevant token that can be used to track the customer and store the Tracardi Profile ID and
Session ID within the defined user session. This ensures that the data collected by Tracardi can be accurately
associated with the correct customer profile and used for further personalization or analysis.

It is essential to follow these steps diligently when integrating Tracardi with mobile apps or external systems to
ensure seamless tracking and utilization of customer data for effective marketing automation and personalization.