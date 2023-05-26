# Forcing profile ID on the page

Sometimes you want to make sure that you track a specific user's activity. This can be useful when redirecting from
emails or other sources. If you already have the customer's profile because the email was sent from Tracardi, you may
want to track that same profile when the user clicks on the link. To do this, you need to enable the static Profile ID
in the event source that collects data and add the profile ID to the page's URL.

It's important to note that this profile tracking will only work if the tracking script is on the page you redirect the
user to. If the page doesn't have this script, you can refer to the documentation for information on Redirected Links
Bridge.

## Example

For example, by adding the "__tr_pid" and "__tr_src" parameters to the URL, which contain the current profile ID and
source ID, the system will create a session for the specified profile if it already exists. There are some conditions
for this to work. If the system already has a profile saved in the browser's local storage, it will try to merge the
previous history of events on that page with the new profile ID and its history. If the user is visiting your page for
the first time, there shouldn't be any issues.

Remember that if a session number is provided, the event will be associated with the corresponding profile. If only a
profile ID is given, a new session will be created for that profile.