# Corporate reputation plugin

This plugin sends given text to MeaningCloud's Corporate reputation API to analyze it for included opinions about
companies.

## Input

This plugin takes any payload as input.

## Outputs

This plugin returns response from API on port **response**, or optional error info on **error** port if one occurs.

## Plugin configuration

- MeaningCloud resource - select your MeaningCloud resource, containing your MeaningCloud API token.
- Path to text - type in the path to the text that you want to analyze.
- Path to language - type in the path to the language of the text (**es**, **en**)
  you can type the language itself as well. This option can be left as **auto** for automatic language detection.
- Focus on company - you can optionally provide a name of company for API to focus on when analyzing your text.
- Filter by company type - you can filter your results by company type. It should be provided according
  to [MeaningCloud's ontology](https://www.meaningcloud.com/developer/documentation/ontology#ODENTITY_ORGANIZATION).
- Relaxed typography - You can enable this option to make the API less strict in terms of spelling and mistakes.

#### Advanced configuration

```json
{
  "source": {
    "name": "<name-of-your-meaningcloud-resource>",
    "id": "<id-of-your-meaningcloud-resource>"
  },
  "text": "<path-to-text-to-analyze>",
  "lang": "<path-to-language-or-language-itself>",
  "focus": "<name-of-company-to-focus-on>",
  "company_type": "<type-of-company-to-filter-with>",
  "relaxed_typography": "<bool>"
}
```