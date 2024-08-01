# What are the differences in Data Flow for Open-source and Commercial Version of Tracardi

Here is the outline the differences between an open-source Tracardi and a Commercial
Tracardi, especially focusing on the differences in data flow, specifically regarding the new version 0.8.2. 

In an open-source Tracardi, we have the following data flow:

1. A request is made to the API, where we collect the tracker payload. The tracker payload basically consists of data in
   the form of profile, session, and event payloads. There may be multiple event payloads for a single profile, with
   potentially as many as 100 events per profile. This illustrates how data is bulked together.

2. The data is then preprocessed and split into events, profiles, and sessions within the system. It is subsequently
   sent to the workflow for processing.

3. Within the workflow, an internal state is maintained, including the event, profile, and session data. The result of
   the workflow, along with any modifications to the event, profile, and session, is saved into the database.

4. Finally, the event or profile is sent to a destination via outbound traffic, and a response is generated. This
   process operates as a single work unit, requiring completion before a response is issued. Consequently, if a workflow
   takes a long time to process, it can result in extended processing times.

Pros of this approach:

- Easy setup with just one Docker installation.
- Ability to add personalized content and await responses within the workflow.
- Simplified maintenance of both the system and the code.

Cons of this approach:

- Limited scalability as everything must be scaled together.
- Limited data access as data can only be fetched from the database.
- Lack of easy extensibility for specific components, as extensions often pollute the code.
- Lower performance due to increased processing time as more elements are added to the workflow or outbound traffic.

There is also a commercial version with a different approach:

1. In the commercial version, there is a foreground process in the server and a background process. The request and
   tracker payload, including profile and event payloads, are processed similarly.

2. However, in this version, the user does not need to wait for everything to complete. The preprocessed data is
   provided quickly as a response.

3. The result of preprocessing includes event, profile, and session data. Deltas are used to describe how the profile is
   updated.

4. In the background, event, profile, and session data are created and sent to a workflow stream. This stream, which
   utilizes Apache Pulsar, stores the data and connects to a worker for processing. Additional workers can be added as
   needed, allowing for scalable processing.

5. The output of this processing goes to a collector, which aggregates and outputs profile and session information at
   regular intervals.

6. Computed profiles and sessions are sent to their respective streams, where they can be connected to additional code
   for further processing.

7. Events, which are immutable, are sent directly to the event stream and then to the database.

8. Another important component is responsible for determining when it's appropriate to process data, ensuring that
   metrics are computed efficiently, and sending profile data to external systems.

9. This approach optimizes data processing, reducing stress on both the database and external systems.

In summary, the commercial version offers faster responses by separating foreground and background processing, as well
as improved scalability and flexibility in handling data streams. It provides better performance and reduces stress on
the database and external systems. Additionally, failures in various components can be handled more effectively.