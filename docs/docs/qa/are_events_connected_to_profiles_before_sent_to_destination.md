# Are events linked to profiles before they are sent to the destination in the data integration process?

Yes, in the data integration process, events are linked to profiles before being sent to the destination. Each event is
assigned a profile ID and session ID, ensuring that by the time the events reach the stream or warehouse destination,
they are appropriately associated with the correct profiles. This pre-linkage of events to profiles is essential for
keeping the data organized and relevant within the warehouse.