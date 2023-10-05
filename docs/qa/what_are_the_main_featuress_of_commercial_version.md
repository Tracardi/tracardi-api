# What are the main features of commercial vs open-source version?

| Feature                                           | Open source | Commercial |
|---------------------------------------------------|-------------|------------|
| __Data collection__                               |             |            |
| * API bridge                                      | x           | x          |
| * Redirect bridge                                 |             | x          |
| * Maintaining the profile id between domains      |             | x          |
| * Kafka bridge                                    |             | x          |
| * MQTT Bridge                                     |             | x          |
| __Data mapping__                                  |             |            |
| * Event to profile mappings                       | x           | x          |
| * Event validation                                |             | x          |
| * Event reshaping                                 |             | x          |
| * Event remapping                                 |             | x          |
| __Profile identification__                        |             |            |
| * Profile merging                                 | x           | x          |
| * Profile identification points                   |             | x          |
| * Data compliance                                 |             | x          |
| * Profile consents                                | x           | x          |
| __Data storage__                                  |             |            |
| * Events                                          | x           | x          |
| * Sessions                                        | x           | x          |
| * Profiles                                        | x           | x          |
| * Entities                                        |             | x          |
| __Destinations__                                  |             |            |
| * Event destinations                              |             | x          |
| * Profile destinations                            |             | x          |
| __Workflow triggers__                             |             |            |
| * Workflow triggered by event                     | x           | x          |
| * Workflow triggered by time                      |             | x          |
| * Workflow triggered by segmentation              |             | x          |
| * Workflow skipped if no consent                  |             | x          |
| __Segmentation__                                  |             |            |
| * Simple segmentation based on profile data       | x           | x          |
| * Segmentation based on event data                |             | x          |
| * Segmentation by workflow                        |             | x          |
| __Profile data enhancement__                      |             |            |
| * Profile metrics                                 |             | x          |
| * Auto profile geo location                       |             | x          |
| __Automation__                                    |             |            |
| * Workflow automation                             | x           | x          |
| * Standard automation actions                     | x           | x          |
| * Time based automation                           |             | x          |
| * AI features, vector stores                      |             | x          |
| * Geo location features                           |             | x          |
| * Automation based on event aggregations          |             | x          |
| * UIX widgets                                     |             | x          |
| * Interactions with Twilio, varius databases, etc |             | x          |
| __Other__                                         |             |            |
| * Multi-tenancy                                   |             | x          |
| * Performance improvements                        |             | x          |
| * Automatic profile visits closing                |             | x          |
| * Post collection data indexing                   |             | x          |

