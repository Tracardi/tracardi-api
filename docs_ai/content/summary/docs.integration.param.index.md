The documentation provided explains how to enable the static Profile ID in the event source that collects data and add
the profile ID to the page's URL. This is useful when redirecting from emails or other sources and you want to track a
specific user's activity. To do this, you need to add the "__tr_pid" and "__tr_src" parameters to the URL, which contain
the current profile ID and source ID. This will create a session for the specified profile if it already exists.

It's important to note that this profile tracking will only work if the tracking script is on the page you redirect the
user to. If the page doesn't have this script, you can refer to the documentation for information on Redirected Links
Bridge. If the system already has a profile saved in the browser's local storage, it will try to merge the previous
history of events on that page with the new profile ID and its history. If the user is visiting your page for the first
time, there shouldn't be any issues. Remember that if a session number is provided, the event will be associated with
the corresponding profile. If only a profile ID is given, a new session will be created for that profile.