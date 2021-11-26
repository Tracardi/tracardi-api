# Url parser plugin

This plugin parses URL and returns it as output.

# Configuration

User must provide a path to page URL. By default, path is available at `session` in `context.page.url`

```json
{
  "url": "session@context.page.url"
}
```

# Input

This action does not process input payload directly.

# Output

Output example for url `http://web.address.com/path/index.html?param1=1#hash`:

```json
{
  "url": "http://web.address.com/path/index.html?param1=1#hash",
  "scheme": "http",
  "hostname": "web.address.com",
  "path": "path",
  "query": "index.html?param1=1",
  "params": {
    "param1": "1"
  },
  "fragment": "hash"
}
```