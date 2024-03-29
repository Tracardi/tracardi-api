# What plugins has Tracardi?

Here is a list of Tracardi plugins:

* Enrich profile: This plugin retrieves data about the provided e-mail from FullContact service. (Version: v0.6.1)
* HTML fetcher: Fetches HTML page. (Version: v0.6.1)
* MSN Weather service: Retrieves weather information. (Version: v0.6.1)
* Remote API call: Sends a request to a remote API endpoint. (Version: v0.8.0)
* Send e-mail via SMTP: This plugin sends mail via the defined SMTP server. (Version: v0.7.3)
* Send tweet: Create and send a tweet to your Twitter wall. (Version: v0.8.0)
* Whois: Checks the domain in the WHOIS service. (Version: v0.8.0)
* Assign profile id: Assigns a new profile id to the event. (Version: v0.6.2)
* Create empty profile: Adds a new profile to the event. An empty profile gets created with a random id. (Version: v0.8.0)
* Create empty session: Adds a new session to the event. An empty session gets created with a random id. (Version: v0.7.0)
* Delayed event: Raises an event that is delayed X seconds after the customer visit ends. (Version: v0.6.2)
* Discard profile update: Stops the update of the profile in storage. (Version: v0.7.3)
* Generate password: Generates a new password according to user input. (Version: v0.7.1)
* Get OAuth2 token: Gets OAuth2 token from the given endpoint, using the given username and password. (Version: v0.6.1)
* Get field type: This plugin returns the type and length (if it exists) of the given field. (Version: v0.7.1)
* Hash data: Hashes defined data, e.g., profile traits. (Version: v0.7.0)
* Join: Joins input data into one payload. (Version: v0.7.1)
* Load profile by ...: Loads and replaces the current profile in the workflow. It also assigns the loaded profile to the current event. It basically replaces the current profile with the loaded one. (Version: v0.7.2)
* Mask data: Masks defined data, e.g., profile traits. (Version: v0.7.0)
* Merge profiles: Merges profiles in storage when the flow ends. This operation is expensive, so use it with caution, only when there is new PII information added. (Version: v0.8.0)
* Payload collector: Collects input payloads in the workflow memory object. (Version: v0.7.1)
* Reduce array: Reduces the given array. (Version: v0.6.2)
* Sort dictionary: Sorts the referenced dictionary and returns it as a list of tuples of key and value. (Version: v0.7.3)
* Sort list: Plugin that sorts (ascending, descending) a referenced array/list. (Version: v0.7.3)
* Tag event: Adds a tag to the current event. (Version: v0.8.0)
* UUID4: Generates a random UUID. (Version: v0.6.2)
* Update event: Updates the event in storage. (Version: v0.6.0.1)
* Update profile: Updates the profile in storage. (Version: v0.6.0.1)
* Update session: Updates the session in storage. (Version: v0.6.2)
* Data exists: Checks if the data property exists and is not null or empty. (Version: v0.8.0)
* If: This is a conditional action that conditionally runs a branch of the workflow. (Version: v0.7.4)
* Is it a new profile: If new profile then it returns true on TRUE output, otherwise returns false on FALSE port. (Version: v0.6.0.1)
* Is it a new visit: If new visit then it returns true on TRUE output, otherwise returns false on FALSE port. (Version: v0.6.0.1)
* Limiter: This node throttles the workflow execution. (Version: v0.7.3)
* Resolve conditions: That plugin creates an object with results from resolved condition set. (Version: v0.6.2.1)
* Resolve conditions into profile fields: This plugin resolves a set of conditions and assigns it to the profile fields. (Version: v0.6.2)
* Value change: This plugin will stop the workflow if the defined value did not change. (Version: v0.6.1)
* Discard Event: Discards the current event - Current event will not be saved if this action is used. (Version: v0.7.1)
* Event aggregator: This plugin collects and tallies up the occurrences of a specific category of information during a certain period of time for the current profile. (Version: v0.8.0)
* Event counter: This plugin reads how many events of the defined type were triggered within the defined time. (Version: v0.8.0)
* Get previous event: Injects the previous event for the current profile into the payload, according to the event type and offset value. (Version: v0.6.2)
* Inject event: This node will inject an event of a given ID into the payload. (Version: v0.6.0.1)
* Add interest: Adds interest to the profile. (Version: v0.8.0)
* Add segment: Adds a segment to the profile. (Version: v0.7.3)
* Conditional segmentation: This plugin will add/remove a segment from the profile. (Version: v0.6.0.1)
* Decrease interest: Decreases interest in the profile and returns the payload. (Version: v0.8.0)
* Delete segment: Deletes a segment from the profile. (Version: v0.7.3)
* Force segmentation: Segment profile when flow ends. This action forces segmentation on the profile after the flow ends. See documentation for more information. (Version: v0.6.0.1)
* Has segment: Checks if the profile is in the defined segment. (Version: v0.7.3)
* Increase interest: Increases interest in the profile and returns the payload. (Version: v0.8.0)
* Memorize segment: Memorize profile segments in workflow memory. (Version: v0.7.3)
* Move segment: Moves the profile from one segment to another segment. (Version: v0.7.3)
* Recall segment: Loads memorized profile segments into the output payload. (Version: v0.7.3)
* Create entity: Adds or updates an entity. (Version: v0.7.3)
* Delete entity: Deletes an entity by its ID. (Version: v0.7.2)
* Load entity: Loads an entity by its ID. (Version: v0.7.3)
* Get event source: This plugin reads the source that the event came from. (Version: v0.6.0.1)
* Inject: Injects data into the selected object (e.g., payload, event properties, session context, etc). (Version: v0.6.2)
* Inject payload: Creates a new payload from the provided data. Configuration defines where the data should be copied. (Version: v0.8.0)
* Load report data: Loads the results of a given report into the payload. (Version: v0.7.2)
* Load report data: Loads the results of a given report into the payload. (Version: v0.7.2)
* Novu notifications: Create and send notifications to chosen recipients. (Version: v0.7.2)
* Add to audience: Adds a contact to MailChimp audience. (Version: v0.6.0.1)
* Remove from audience: Removes or archives a contact from the MailChimp audience. (Version: v0.6.0.1)
* Send e-mail: Sends transactional e-mail via MailChimp API. (Version: v0.6.0.1)
* Count records: Counts event, profile, or session records. Records can be filtered by a query string. (Version: v0.6.2)
* Decrement counter: Decrements the profile stats.counters value and returns the payload. (Version: v0.1)
* Increase views: Increases the view field in the profile and returns the payload. (Version: v0.1)
* Increase visits: Increases the visit field in the profile and returns the payload. (Version: v0.1)
* Increment counter: Increments the given field in the payload and returns the payload. (Version: v0.1)
* Key counter: Counts keys and saves them in the profile. (Version: v0.6.0.1)
* Contains pattern: Checks if a field contains the defined pattern. (Version: v0.7.2)
* Contains string: Checks if a field contains the defined string. (Version: v0.7.2)
* Data validator: Validates data such as email, URL, IPv4, date, time, int, float, phone number, EAN code. (Version: v0.6.0.1)
* Ends with: Checks if a string ends with the defined prefix. (Version: v0.7.2)
* Join string list: Joins each element in the list by the given delimiter. (Version: v0.7.3)
* Starts with: Checks if a string starts with the defined prefix. (Version: v0.7.2)
* String properties: Performs string transformations like lowercase, remove spaces, split, and more. (Version: v0.6.0.1)
* String similarity: Compares two strings according to the chosen algorithm. (Version: v0.7.3)
* String splitter: Splits a string into a list of strings by the defined delimiter. (Version: v0.6.0.1)
* Append/Remove data: Appends or removes a trait to/from the given destination. (Version: v0.1)
* Calculator: Calculates new values by adding, subtracting, dividing, and multiplying values. (Version: v0.6.0.1)
* Copy data: Copies event properties to a profile trait. (Version: v0.6.0)
* Create response: Creates a new response from the provided data. Configuration defines where the data should be copied. (Version: v0.7.2)
* Cut out data: Returns a part of referenced data as payload. (Version: v0.8.0)
* Delete data: Deletes data from the internal state of the workflow. (Version: v0.1)
* Detect device: Parses a user agent string and detects the browser, operating system, and device used. (Version: v0.6.1)
* Merge event properties: Automatically merges all event properties to profile traits. (Version: v0.6.2)
* Random item: Returns a random value from the list given in the configuration. (Version: v0.6.1)
* Template: Returns a string where placeholders are replaced with given values. (Version: v0.6.0.1)
* Value mapping: Returns a matching value from the set of data. (Version: v0.6.1)
* XPATH HTML Scrapper: Scrapes data from HTML content. (Version: v0.6.1)
* Log message: Logs a message to the flow log. (Version: v0.6.1)
* Throw error: Throws an error and stops the workflow. (Version: v0.6.0.1)
* Geo distance: Determines if the test geo location coordinates are within the radius threshold from the center point coordinates. (Version: v0.6.1)
* Geo fence: Determines if the test geo location coordinates are within the radius threshold from the center point coordinates. (Version: v0.6.1)
* GeoIp service: Converts IP to location information. (Version: v0.6.1)
* Discard Profile: Discards the current profile - the current profile will not be saved if this action is used. (Version: v0.8.0)
* Discard Session: Discards the current session - the current session will not be saved if this action is used. (Version: v0.8.0)
* Get previous session: Loads previous sessions for the current profile and injects them into the payload. (Version: v0.6.2)
* Regex match: Uses regex matching and returns matched data. (Version: v0.6.0.1)
* Regex replace: Replaces a substring that matches a regex pattern with the given replacement string. (Version: v0.6.1)
* Regex validator: Validates data with a regex pattern. (Version: v0.6.0.1)
* JSON schema validator: Validates objects using the provided JSON validation schema. (Version: v0.7.4)
* Regex validator: Validates data with a regex pattern. (Version: v0.6.0.1)
* Parse URL: Reads URL parameters from the context, parses them, and returns the result on the output. (Version: v0.6.0.1)
* Day/Night: Splits the workflow based on whether it is day or night at the given latitude and longitude. (Version: v0.6.0.1)
* If it's a weekend: Checks the current date and flags it if it's a weekend or not. (Version: v0.7.2)
* Is time between dates: Checks if the current time is within a defined time span. (Version: v0.6.0.1)
* Last profile visit time: Returns the time difference between the last profile visit and the current time. (Version: v0.7.3)
* Pause and Resume: Waits for X seconds and then restarts the workflow at this node. (Version: v0.8.0)
* Profile live time: Returns how long ago a profile was registered in the system. (Version: v0.8.0)
* Sleep: Stops the workflow for a given time. (Version: v0.1.2)
* Time difference: Returns the time difference between two dates. (Version: v0.6.0.1)
* Today: Returns information about the current time, month, day, etc. It consists of the day of the week, date, and current time. (Version: v0.1.1)
* Custom widget: Shows a custom JavaScript widget. (Version: v0.8.0)
* OpenReplay: Injects the OpenReplay tracing script on the webpage. (Version: v0.8.0)
* Rating widget: Shows a rating widget with a defined title and content. (Version: v0.8.1)
* Request demo widget: Shows a request demo widget. (Version: v0.8.1)
* Show consent bar: Shows a consent pop-up on the frontend. (Version: v0.6.1)
* YouTube widget: Shows a YouTube video widget. (Version: v0.8.1)
* Telegram message: Sends a Telegram message via the bot. (Version: v0.8.0)
* Google Analytics 4 event: Send your custom event to the Google Analytics 4 event tracker. (Version: v0.7.3)
* Google Spreadsheet: This plugin connects Tracardi to Google Sheets. (Version: v0.6.1)
* Google Translate: Translates text. (Version: v0.7.2)
* Google UA events: Send your customized event to the Google Universal Analytics event tracker. (Version: v0.8.0)
* End: Ends the workflow. (Version: v0.1)
* Start: Starts the workflow and returns event data on the payload port. (Version: v0.8.0)
* Add contact: Creates or updates a contact in ActiveCampaign, according to the provided configuration. (Version: v0.6.3)
* Fetch contact: Fetches ActiveCampaign contact info based on the given email address. (Version: v0.6.3)
* Register event: Sends the current event to Matomo. (Version: v0.6.2)
* Data to JSON: Converts objects to JSON. (Version: v0.6.0.1)
* Decode Base64: Decodes a base64-encoded input to plain text. (Version: v0.7.3)
* Encode Base64: Encodes input text to base64. (Version: v0.7.3)
* JSON to data: Converts JSON to data objects. (Version: v0.6.2)
* Discord push: Sends a message to a Discord webhook. (Version: v0.7.4)
* Post to Slack Channel: Posts a defined message to a Slack channel. (Version: v0.6.1)
* Pushover push: Connects to the Pushover app and pushes a message. (Version: v0.7.1)
* Microservice: Runs a remote microservice plugin. (Version: v0.7.2)
* Add consent: This plugin adds consents to the profile. (Version: v0.6.3)
* Require consents: Checks if defined consents are granted by the current profile. (Version: v0.6.2)
* Get Issue: Get single GitHub issue details. (Version: v0.7.4)
* List Issues: Lists GitHub issues. (Version: v0.7.4)
* Query data: Query local Elasticsearch database. (Version: v0.8.0)
* Send SMS: Sends an SMS using the Twilio gateway. (Version: v0.8.1)
* Event sequence: This plugin returns an events sequence from the database for a defined time range and context. (Version: v0.8.0)
* Event sequence match: This action will look for a sequence of events in a delivered list of events. (Version: v0.8.0)
* ChatGPT prompt: Sends a request to ChatGPT and returns the response. (Version: v0.8.0)