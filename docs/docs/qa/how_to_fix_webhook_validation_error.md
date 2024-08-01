# I have ValidationError when calling webhook

If you see: 1 validation error for EventPayload\nproperties\n  value is not a valid dict (type=type_error.dict) That means 
that you did not send a post payload as dict. Dict in python is an JavaScript object. Please, send an empty object in 
post body/payload e.g. {} or any object with data: {“key”:”value”}.
