# Parse URL

This plugin is designed to read a URL from the context provided within a workflow and extract various components of the
URL, such as the scheme, hostname, path, query parameters, and fragment.

# Version

0.6.0.1

## Description

When this plugin is activated, it begins by locating a specific URL within the workflow's context. It then proceeds to
dissect the URL into its constituent parts. Each section of the URL, from the scheme (like HTTP or HTTPS) to the
individual query parameters, is separated and cataloged. The result is a structured representation of the URL, with each
element neatly organized for easy reference.

Here's a step-by-step description of what the plugin does:

1. It takes a URL from the workflow's context or session data.
2. It analyzes the URL, separating it into the scheme, hostname, path, query string, individual query parameters, and
   fragment (also known as the hash).
3. It constructs an output that is a detailed map of all these parts for use in subsequent steps of the workflow.

For example, if the plugin is given a URL like **http://web.address.com/path/index.html?param1=1#hash**, it will produce
an output that organizes the URL's components into a structured format:

```json
{
  "url": "http://web.address.com/path/index.html?param1=1#hash",
  "scheme": "http",
  "hostname": "web.address.com",
  "path": "/path/index.html",
  "query": "param1=1",
  "params": {
    "param1": "1"
  },
  "fragment": "hash"
}
```

# Inputs and Outputs

The plugin receives data through a single input port named "payload". However, it does not process this input payload
directly; instead, it uses it to access the URL from the workflow's context.

The output is then passed on through a port, also named "payload", and includes the parsed URL data in a structured
format.

This plugin is not a starting point in a workflow; it requires some data to be passed into it to function.

# Configuration

To configure this plugin, the following parameter must be set:

- __Path to page URL__: You need to specify the path to the page URL. The default location for this is within the
  session's context, specifically at **context.page.url**.

# JSON Configuration

Here is an example of a JSON configuration for this plugin:

```json
{
  "url": "session@context.page.url"
}
```

# Required resources

This plugin does not require external resources to be configured.

# Errors

This plugin documentation does not include any specific errors or exceptions. However, general errors may occur if the
URL path is not correctly specified or if the URL format is not valid for parsing. Ensure that the URL path is correctly
provided and that the URL is in a standard, parseable format to avoid these issues.