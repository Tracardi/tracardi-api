# XPATH HTML Scrapper

The XPATH HTML Scrapper plugin is used to extract specific data from HTML content using the XPATH syntax. 

# Version

The documented version of this plugin is 0.6.1.

## Description 

This plugin is for scrapbooking data from HTML content. It uses XPATH to point to the data you want to scrap. The plugin works by accepting an HTML payload input and then using the XPATH provided in the configuration, it navigates the HTML and extracts the targeted data. The result is returned on the "result" port.

If the plugin does not find data at the provided XPATH, an error occurs. The error message along with the plugin configuration details are returned on the "error" port. 

# Inputs and Outputs

This plugin accepts a payload object on its input port and gives out its results on two output ports:

- **result**: This port returns the scraped data from the HTML content.
- **error**: If the plugin is unable to scrape data, it returns the plugin configuration along with the error message. 

The plugin cannot start a workflow because it requires an HTML payload input to function. 

# Configuration

The plugin requires you to configure the following fields:

- __xpath__: The XPATH that points to the data you would like to scrape from the HTML.
- __content__: The path to the HTML content.

# JSON Configuration

Below is an example of how the plugin can be configured:

```markdown
{
    "xpath": "//div[@class='myClass']",
    "content": "event@data.html"
}
```
This configuration tells the plugin to extract the data within a div tag with the class name 'myClass' from the HTML content accessed through the event@data.html path.

# Required resources

This plugin does not require external resources to be configured.

# Errors

The plugin could throw an error that states: "Could not find any data at path '<your_xpath>'". This error may occur when the XPATH provided in the configuration does not match any element in the HTML content. The error message is returned with the plugin configuration details for debugging.