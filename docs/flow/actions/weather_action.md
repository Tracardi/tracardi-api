# Weather plugin

This plugin connects to weather server and retrieves weather information.

# Configuration

First you need to configure what type of temperature you need. Either in Celsius (C) of Fahrenheit (F)

Example of configuration.

```json
{
  "system": "C",
  "city": "profile@traits.public.city"
}
```

City can ba a path to data or a plain text.

```json
{
  "city": "Paris"
}
```

# Input

Input payload is not processed by this plugin.


# Output

*Example*

```json
{
  "temperature": 4,
  "humidity": 87,
  "wind_speed": 15,
  "description": "Sunny"
}
```