# How tracardi process event context

This documentation describes in detail how Tracardi retrieves event context and profile geo location, utm parameters, etc.

## Description

The code for retrieving the profile's geo location in Tracardi follows the following steps:

1. It first checks if the session is new by evaluating the `session.is_new()` condition. If the session is
   new, it proceeds with the following steps. If not, it skips the subsequent steps and moves to the next part of the
   code.

2. When a new session is detected, the code adds a "session-opened" event to the list of registered events. This event
   signifies the creation of a new session.

3. The code then retrieves the user agent data from the session's context. The user agent data provides information
   about the user's browser, device, and operating system. It extracts the user agent string from the session's context
   and parses it using the `parse` function.

4. From the parsed user agent data, the code extracts various device-related information such as the operating system
   version, operating system name, and device type. The device type can be "mobile," "pc," "tablet," or "email" based on
   the user agent data.

5. Next, the code checks if the session's context contains additional device information under the "device" key. If
   present, it uses that information to populate the session's device properties such as device name, brand, model,
   touch capability, and device type. If the session's context does not have device information, the code uses the
   corresponding values from the parsed user agent data.

6. The code then retrieves the spoken languages from the request headers and the geo country code from the device's geo
   information. It looks for the "accept-language" header in the tracker payload's request headers and parses the
   languages using the `parse_accept_language` function. It filters out languages with a length of 2 characters and maps
   them to the corresponding spoken languages using a predefined dictionary. The code also checks if the device's geo
   information includes a country code and maps it to spoken languages using the same dictionary. The resulting spoken
   languages are set as the session's language context and stored in the profile's "pii.language.spoken" field.

7. If the profile's auxiliary data does not contain a "geo" field, the code initializes it as an empty dictionary.

8. The code determines the continent based on the timezone information present in the tracker payload's context. It
   extracts the timezone value and checks if it is in UTC or a specific region. If it is in a specific region, the code
   splits the timezone string and retrieves the continent. The continent is then stored in the profile's auxiliary data
   under the "geo.continent" key.

9. The code identifies the markets based on the language codes obtained earlier. It checks if the language codes exist
   in a predefined dictionary that maps language codes to market values. If there are matching market values, they are
   added to the profile's auxiliary data under the "geo.markets" key.

10. The code tries to retrieve additional screen-related information from the tracker payload's context. It retrieves
    the screen resolution, color depth, and orientation if available, and assigns them to the session's device
    properties.

11. The code determines if the session's device is a bot by checking the user agent data. If the user agent indicates
    that it is a bot, the session's "app.bot" property is set to `True`.

12. The code extracts the browser name from the user agent data and assigns it to the session's "app.name" property. It
    also retrieves the browser version and assigns it to the session's "app.version" property. The session's "app.type"
    property is set to "browser" to indicate that it is a browser application.

13. If the tracker payload's context contains UTM parameters, the code creates a UTM object from the context data and
    assigns it to the session's "utm" property. The UTM parameters are used for tracking the source of the incoming
    traffic.

14. The code attempts to retrieve the device's IP address from the request headers. It looks for the "x-forwarded-for"
    header and assigns its value to the session's device IP property.

15. Lastly, the code tries to retrieve the browser's language from the session's context and assigns it to the
    session's "app.language" property.

After completing the above steps, the code checks if the location information is available in the tracker payload's
context. If it is present, the code proceeds with the following steps. Otherwise, it skips to the next part of the code.

16. The code validates and parses the location information using the `Geo` class. If the validation succeeds, the code
    removes the location data from the tracker payload's context.

17. If the session's device geo information is empty, indicating that no geo information has been assigned yet, the code
    updates it with the new location data. This ensures that the session's device geo information is populated with the
    latest available location.

18. The code updates the profile's last device geo information if the new location data is different from the existing
    one. This ensures that the profile's last device geo information reflects the most recent geo location.

Finally, the code handles the scenario where there is no geo location available, but the session's device IP address is
present. It checks if the necessary environment variables, namely `MAXMIND_LICENSE_KEY` and `MAXMIND_ACCOUNT_ID`, are
set. If these variables are available, the code proceeds with the following steps. Otherwise, it skips the remaining
part.

19. If the profile's last device geo information is empty, indicating that no geo location has been assigned yet, the
    code fetches the geo location using the MaxMind API. It creates a `GeoLiteCredentials` object with the MaxMind
    license key and account ID and calls the `get_geo_maxmind_location` function with the session's device IP address.

20. The fetched geo location is assigned to the profile's last device geo information, ensuring that it reflects the
    newly obtained geo location.

21. If the session is new, indicating that the user has just initiated the session, the code fetches the geo location
    using the MaxMind API. It assigns the obtained geo location to the session's device geo information and updates the
    profile's last device geo information if it is empty or different from the new location.

22. If there is an error while fetching the geo location using the MaxMind API, the code logs the error message.

The code for retrieving the profile's geo location in Tracardi follows the logic described above, enabling the system to
determine and update the geo location information associated with the profile based on the available data from sessions,
user agents, headers, and external APIs.

