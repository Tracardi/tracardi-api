# Do I need to keep copy data and merge profile actions in one workflow?

If you are using the "Event to profile mapping" feature, you typically wouldn't need the "Copy data" action in your
workflow, as all the necessary data should already be available (mapping happens before workflow). This implies that 
"Copy data" is more suitable for situations where you need conditional copying of data.

We advise that if you opt to use "Copy data," it should be kept in the same workflow as the "Merge profile" action. This
recommendation is based on the lack of a guaranteed sequence in which separate workflows might run, which could lead to
profiles being merged before the data is copied to them. Mapping data to a profile from an event is a preferable option,
as this happens before the workflow starts.

The best practice would be to:

1. Use "Event to profile mapping" wherever possible to avoid the need for a separate "Copy data" action.
2. If "Copy data" is necessary, include it in the same workflow as the "Merge profile" action to ensure proper
   sequencing and avoid potential issues with data not being present at the time of merging.