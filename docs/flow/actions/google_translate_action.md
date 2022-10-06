# Google translate plugin

This plugin translate the delivered text to English .

__CAUTION__: This plugin is __experimental__. It is based on the library **googletrans** which may stop working because it uses
the public JSON API which is not intended for this kind of use.

# JSON Configuration

```json
{
  "text_to_translate": "veritas lux mea",
  "source_language": "la"
}
```


# Output 

Returns result on the output port in the following schema:

```json
{
  "translation": "translated text"
}
```

