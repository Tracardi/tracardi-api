# Text Classification

This plugin classifies provided text.

# Configuration

```json
{
  "source": {
    "name": "Text classification",
    "id": "e7a3979e-7f31-452b-a571-8ca613de77fb"
  },
  "language": "en",
  "model": "press",
  "title": "The iPhone 13 isn’t a game changer",
  "text": "The iPhone 13 isn’t a game changer for Apple’s series of smartphones, but it’s an ..."
}
```

* *source.id* - Id that points to resource with an access token. See below for resource configuration schema.
* *language* - language of the text to classify. (en|sp|it|pt|ct|fr)
* *title* - optional title of the text
* *text* - text to classify

## Resource configuration

```json
{
  "token": "dgrhfcd6hhdj706..."
}
```

# Output

*Example*

```json
{
  "categories": [
    {
      "code": "13016000",
      "label": "science and technology - electronics",
      "abs_relevance": "0.2833175",
      "relevance": "100"
    }
  ]
}
```
