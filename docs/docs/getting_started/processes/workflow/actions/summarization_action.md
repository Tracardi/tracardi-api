# Summarize text plugin

This plugin sends given text to MeaningCloud's summarization API to summarize
it.

## Input
This plugin takes any payload as input.

## Outputs
This plugin returns response from API on port **response**, or optional error
info on **error** port if one occurs.

## Plugin configuration
#### With form
- MeaningCloud resource - select your MeaningCloud resource, containing your MeaningCloud
  API token.
- Path to text - type in the path to the text that you want to summarize.
- Path to language - type in the path to the language of the text (**es**, **en**)
  you can type the language itself as well. This option can be left as **auto** for automatic
  language detection.
- Sentences - type in the number of sentences for text to be summarized to. This field does
  not support dotted notation.

#### Advanced configuration
```json
{
  "source": {
    "name": "<name-of-your-meaningcloud-resource>",
    "id": "<id-of-your-meaningcloud-resource>"
  },
  "text": "<path-to-text-to-analyze>",
  "lang": "<path-to-language-code-or-language-itself>",
  "sentences": "<numeric-string>"
}
```