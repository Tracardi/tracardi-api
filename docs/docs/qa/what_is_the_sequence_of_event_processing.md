# What is the sequence of event processing

Event processing depends on the type of processing. There are 2 types: Asynch, and Synch

ina synchronous processing event is collected by API and:

1. Data source is checked
2. Event  is validated. Validation is performed over the raw/original data.
3. Event is reshaped. Now event can changed to the required format.  
4. Profile Id is extracted and profile properties are extracted and matched for profile identification
5. Event is remapped some data may be now indexed
6.  Event is saved

---
Workflow starts
Dispatching to destinations start
