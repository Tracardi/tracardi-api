# HTML fetcher

HTML fetcher is a Tracardi plugin used for fetching an HTML webpage. It can be used to make an HTTP or HTTPS request to
a given URL and return the response as a result. This plugin allows the configuration of request method, headers,
cookies, SSL check and timeout. The fetched webpage's details such as content, status and cookies are returned upon
success operation, while upon any error such as "time-out" error, connection error or response status other
than [200, 201, 202, 203], corresponding error details are informed.

# Version

This documentation is for the HTML fetcher plugin version 0.6.1.

## Description

The HTML fetcher plugin works as follows:

Initially, the plugin's configuration is set up, based on received parameters. The plugin verifies the dictionaries of
cookies and headers, ensuring that all keys & values are string types. Any non-string values will result in plugin
throwing an error with appropriate message.

Upon successful verification, an HTTP client is initiated within the configured timeout limit. Then, it sends a request
to selected URL using specified method (like GET, POST, etc.). In the request, headers and cookies provided in
configuration are included. If "ssl_check" setting is enabled, the request also validates SSL certificate of the page it
is trying to reach.

When the response is received from the server, it's processed and a "result" dictionary is composed, containing status
code of response, content of the fetched page and received cookies.

If the response's status code is one of the successful HTTP codes (200, 201, 202, 203), the fetching operation is
considered successful and "result" is returned. However, if the status code is different, the operation is deemed
unsuccessful and "error" value with description of the error is returned.

# Inputs and Outputs

The HTML fetcher plugin receives a dictionary with payload in its input.

Upon successful operation, it outputs to "response" port the following structure:

```json
{
  "status": <status-code>,
  "content": <fetched-page-content>,
  "cookies": <received-cookies>
}
```

Upon encountering an error, it outputs to "error" port a simple string with description of occurred error.

# Configuration

The HTML fetcher plugin requires the following configuration:

- "method": Request method, can be GET, POST, PUT, or DELETE.
- "url": The URL of the webpage to be fetched.
- "body": Content to be sent in request. Accepts double curly braces for replacing part of content with data, e.g.,
  {{profile@id}}.
- "timeout": The maximum time (in seconds) to wait for a response.
- "headers": A dictionary for request headers.
- "cookies": A dictionary for cookies.
- "ssl_check": A boolean value to determine if the SSL certificate should be checked and validated.

# JSON Configuration

Here is an example of plugin's configuration:

```json
{
  "method": "get",
  "url": "https://example.com",
  "timeout": 30,
  "headers": {
    "Content-Type": "application/json"
  },
  "cookies": {
    "sessionid": "123456"
  },
  "ssl_check": true,
  "body": ""
}
```

# Required resources

This plugin does not require external resources to be configured.

# Errors

The plugin returns several exceptions:

- "Header values must be strings, <given_type> given for header <header_name>": May occur when given headers contain
  non-string values.
- "Cookies values must be strings, <given_type> given for cookies <cookies_name>": Occurs when given cookies contain
  non-string values.
- "Remote call timed out": Occurs when program does not receive response within the configured time limit from requested
  URL.
- Any other error messages returned from aiohttp library, for example capturing __ClientConnectorError__ which is raised
  for connection issues like DNS resolution, refused connection, etc. The detailed error message for such exceptions
  will be directly from the aiohttp library.

Please note that if there aren't any errors, but response's status is not within [200, 201, 202, 203], the plugin
returns a dictionary similar to successful operation, but routes it to "error" port instead.