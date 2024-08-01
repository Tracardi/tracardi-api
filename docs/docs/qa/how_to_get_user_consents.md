# How to collect consents and use consent box widget to obtain customer consents.

1. **Defining Consent Types**: Determine the various consents you need from your customers. These could include
   permissions for marketing communications, data processing, cookie tracking, etc. Categorize these under '
   Identification/Consent Types' in Tracardi.

2. **Creating a Consent Box**: Develop a consent box widget that will be displayed to users, which should:
    - Clearly articulate what the user is consenting to, using the consents defined in Tracardi.
    - Offer options for users to accept or decline specific types of consents.
    - Ensure compliance with relevant regulations, such as GDPR and CCPA.
      You can leverage Tracardi's built-in Consent Bar Widget, which automatically utilizes defined consents.

3. **Integrating the Consent Box**: Embed the consent box into the appropriate user interaction workflow on your
   platform.

4. **Capturing Consent Responses**: Monitor and record the user's interactions with the consent box, whether they accept
   or decline. This can be done using Tracardi, which tracks these interactions as events. The built-in Consent Bar
   Widget in Tracardi automates this process, eliminating the need for manual event setting.

5. **Storing Consent Information**: Preserve the gathered consent information in the user's profile in Tracardi,
   typically within the `consents` key. The built-in widget in Tracardi facilitates automatic storage of this data.

6. **Utilizing Consent Data in Workflows**: Use the stored consent data in your Tracardi workflows to enhance user
   experiences and personalize marketing efforts. For instance, send marketing emails only to users who have explicitly
   consented to receive them.

7. **Anonymizing Data Using Consents**: Employ the consents provided by users to anonymize data as necessary, ensuring
   privacy and compliance with data protection regulations.