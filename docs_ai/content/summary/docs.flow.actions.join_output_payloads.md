This plugin also supports merging of arrays. If the data contains array then it will be merged into one array. 
For example if the payloads look like this:

```json
{
  "data": [1, 2],
  "edge": [3, 4]
}
```

then the result will be:

```json
[1, 2, 3, 4]
```