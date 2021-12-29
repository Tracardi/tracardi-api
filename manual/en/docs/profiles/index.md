# Profile 

## Profile in response

It is **very important** to synchronize `profile.id` returned in response with the profile id saved on a client side. 
When the profile in response is different then the one we have sent that it means that the client should update its 
`profile.id` and send new one with the next call. If you miss this part then the `profile.id` will be recreated with 
each call to /track API. That may ruin the whole profile.