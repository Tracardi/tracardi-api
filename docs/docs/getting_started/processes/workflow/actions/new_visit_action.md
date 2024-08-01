# New visit 

This plugin will return payload on TRUE port if the event indicates that this is a new visit. This usually happens when the customer 
visits site for the first, second, third time, etc. Visit is considered finished whe the user leaves the page and closes the browser.
This plugin will trigger only on the first page view of the visit when a new session is created. Second click within the visit will 
not trigger this action.

# Output

Payload on TRUE or FALSE port depending on if this is a new visit.