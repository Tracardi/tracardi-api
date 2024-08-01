# What Happens When Two Workflows Generate Responses

In a situation where a single event triggers two workflows, both workflows execute and produce responses as their
output. The system consolidates these responses, and if there are no key name conflicts, it will return all the data. In
case of conflicts, the last value will take precedence and override the first value.