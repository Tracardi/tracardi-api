# What are entities and how can I use them.

In Tracardi, entity is concept used for storing and managing data. Tracardi maintains a separate index, which can be
considered as a store or table, specifically designed to hold information about entities. Each entity has a unique type
and associated data.

The entity index in Tracardi allows you to store various types of data, depending on your requirements. For example, you
can store information about email, products, or any other relevant data related to your business or application.

Tracardi provides plugins called "Save Entity" and "Load Entity" that enable you to interact with the entity index
within your workflows. These plugins are available in the commercial version of Tracardi. With the "Save Entity" plugin,
you can save or update data for a specific entity in the entity index. The "Load Entity" plugin allows you to retrieve
the stored data of an entity from the index.

Each entity is related to profile.

It's worth mentioning that if you are using the open-source version of Tracardi and require similar functionality, you
can utilize the "profile@aux" attribute to store data. While it may not provide the same dedicated entity index as in
the commercial version, the "profile@aux" attribute serves as a convenient way to store additional information within a
user's profile. You can leverage this attribute to store and retrieve data similar to how entities work in the
commercial version.

## Difference between Entities and Aux Property

Entities and aux properties in Tracardi have distinct characteristics in terms of their relationship and usage:

* __Relationship__: Entities in Tracardi can be associated with a one-to-many relationship. This means that a single
  profile can have multiple entities associated with it. For instance, you can have an entity called "Purchase"
  associated with a specific user profile, and that user profile can have multiple purchase entities linked to it. This
  allows for storing and managing collections of related data under a single profile.

  On the other hand, the aux property in Tracardi has a one-to-one relationship. Each profile can have its own aux
  property, which serves as an additional attribute associated with that specific profile. The aux property allows you
  to store supplementary information related to the profile, but it is limited to a single set of data per profile.

* __Usage__: Entities are commonly used when dealing with data that has a common theme or relationship but varies in
  quantity. For example, entities can be utilized to store various actions, or interactions related to a customer, where
  each entity represents a specific instance of that action (e.g. Purchase, Sent email).

  Conversely, aux properties are typically employed to store specific details or metadata about a profile that are
  unique to that individual. This can include preferences, additional user information, or any other supplementary data
  that is directly associated with the profile itself.

In summary, the key distinction between entities and aux properties lies in their relationship and usage. Entities can
establish a one-to-many relationship between profiles and associated data, while aux properties maintain a one-to-one
relationship, providing an additional attribute specific to each profile. Understanding this difference allows for
better organization and management of data within Tracardi based on your specific needs.

## Entities as an Extension of Events

It's important to note that the profile is also in a one-to-many relationship with events. This means that a single
profile can have multiple events associated with it. Each event represents a specific action or occurrence related to
the profile, such as a user interaction, a purchase, or any other significant event that you want to track.

Since events capture a wide range of activities, entities can be seen as an extension of events. Entities provide a way
to store additional data that may not be directly tied to a specific event but is still relevant to the profile. In
other words, entities offer a mechanism to store information that doesn't fit neatly into the event structure or you do
not want to keep this information in the event itself.

For example, let's consider a scenario where you want to track purchases made by users. Each purchase can be represented
as an event, and the associated data, such as the item purchased, the price, and the transaction details, can be stored
within the event itself.

However, there might be additional information related to the purchase that doesn't fit well within the event structure.
This could include details like: if the confirmation email was sent by the workflow, or additional notes specific to
that purchase. Instead of trying to raise another event, you can utilize entities to store these supplementary details
and retrieve them when needed. 