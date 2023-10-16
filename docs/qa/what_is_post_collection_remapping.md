# Difference between 'Assign data to profile from event' and a workflow to map data from event to profile

The key difference is when the data is processed. A workflow maps data from events to profiles in real-time as the
events arrive. This ensures that profiles are immediately updated with the latest information. On the other hand, '
Assign data to profile from event' allows you to perform this mapping on already collected events. It's useful when you
haven't set up the mappings initially and want to retrospectively update profiles with historical data.

# Does reindexing simply mean mapping event properties to event traits? If yes, how does it differ from a workflow too

Yes, reindexing involves mapping event properties to event traits, but it is typically done after the data has already
been collected. For instance, if you forgot to index the "purchase order value" and now want to be able to search for
it, you would need to reindex the data. Reindexing updates the data in a batch process, converting properties to traits
for older, already collected data.

In contrast, a workflow maps event data to profiles in real-time as new events arrive. So, while both reindexing and
workflows involve mapping data, the key distinction is that reindexing is a batch process for historical data, whereas
workflows process data as it comes in, keeping profiles updated in real-time.
