# Categorize text plugin

This plugin sends given text to MeaningCloud's Deep categorization API to analyze
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
- Path to text - type in the path to the text that you want to analyze.
- Model - this API analyzes text using different models. Valid models are:
  - IAB_2.0_**language**
  - IAB_2.0-tier3_**language**
  - IAB_2.0-tier4_**language**
  - You can also use these models without _**language** suffix for automatic language detection. 


#### Advanced configuration
```json
{
  "source": {
    "name": "<name-of-your-meaningcloud-resource>",
    "id": "<id-of-your-meaningcloud-resource>"
  },
  "text": "<path-to-text-to-analyze>",
  "model": "<model-name>"
}
```