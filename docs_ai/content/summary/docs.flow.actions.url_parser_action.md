This plugin is designed to parse URLs and return the parsed information as output. The user must provide a path to the
page URL, which is available at the session in context.page.url by default. This action does not process input payload
directly. The output example for a URL such as http://web.address.com/path/index.html?param1=1#hash would be a JSON
object containing the URL, scheme, hostname, path, query, params, and fragment. The params object would contain the
parameter name and value, in this case "param1" and "1" respectively. This plugin is useful for extracting information
from URLs and using it for further processing.