This plugin is designed to extract topics from a given text using MeaningCloud's Topics extraction API. It takes any
payload as input and returns the response from the API on the response port, or an optional error info on the error port
if one occurs.

The plugin can be configured either with a form or with advanced configuration. With the form, the user must select
their MeaningCloud resource, containing their MeaningCloud API token, and type in the path to the text and language of
the text (or type the language itself) that they want to analyze. The language can be left as "auto" for automatic
language detection.

For advanced configuration, the user must provide a JSON object containing the name and ID of their MeaningCloud
resource, the path to the text to analyze, and the path to the language code or language itself.