# Google analytics 4 event tracker

This plugin sends event to google analytics 4

# JSON Configuration

```json
{
  "name": "name",
  "params": "{params_name: params_value}"
}
```

* __Name__ (required): The name of your event, event name describe the action taken on your website. Example: Refund
* __Params__ (required): The parameters of your event which including all details about defined event. Example:
  Currency-USD, you can define many parameters for one event.

# Output

Returns result on the output port in the following schema:

```json
{
  "status": 204,
  "content": "response content"
}
```