# How post event segmentation work?

Post event segmentation works differently from live segmentation as it is triggered by events that update the profile.
Here's an explanation of how post event segmentation works:

* Profile Update: Post event segmentation is initiated when an event occurs and updates the profile.

* Event Type: Post event segmentation is typically configured to run only on specific event types. This means that the
  segmentation process is triggered only when the specified event type occurs. For example, if the event type is "
  purchase," segmentation will be performed only when a purchase event is received and updates the profile.

* Segment Evaluation: Once the event updates the profile, the system evaluates the segment conditions defined in the
  segmentation condition. These conditions can be based on factors, such as profile attributes, traits, or properties.
  The segment conditions define the criteria that profiles must meet to be assigned to a particular segment.

* Segment Assignment: If a profile satisfies the segment conditions, it is assigned to the defined segment.

Overall, post event segmentation is triggered when an event updates the profile. It evaluates the segment conditions and
assigns the profile to the appropriate segment if the conditions are met.

---
This documents answers the following questions:

- My post event segmentation does not work
- How the post event segmentation is different for live segmentation?
- Why my post event segmentation does not work?