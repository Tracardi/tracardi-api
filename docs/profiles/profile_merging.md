# Profile merging and Identity resolution

## Introduction

Profile merging is the process of combining multiple customer profiles that belong to the same person, but have been saved as separate records. This can happen for various reasons such as using different devices, browsers or even different email addresses. In order to combine these data into one record, it is necessary to select a merging key that will be a unique value acress the whole system and by which the customer data could be combined. This can be an email address, credit card, or any other global identifier that can be used to group client profiles.

!!! Example

    For example, if a customer uses their laptop with Firefox browser, they may have one profile with an ID of 1. But when they use the same device but using Google Chrome, they may have another profile with ID of 2. And when they use a mobile phone, they may have a third profile with ID of 3. Even though they are the same person, they have 3 different profiles. Profile ID 1 may have data about their purchases but not their name and surname, while their first and last name may be saved in profile ID 2. Profile merging is needed to aggregate all the fragmented data set into one profile to have a complete understanding of the customer.

## Identity resolution

Identity resolution is a broader term. It is the process of linking multiple pieces of data about a single individual or entity, in order to create a complete and accurate picture of that individual or entity. This can be done using a variety of techniques, such as matching data based on common attributes, using machine learning algorithms to identify patterns in the data, or using external data sources to supplement and verify the data.

In the context of a customer data platform (CDP), identity resolution is used to link together data about a customer from multiple sources, such as website interactions, email campaigns, and customer service interactions, by merging the data.

## Merging process

Merging is a complex process that involves combining multiple customer profiles that belong to the same person. It is done by following rules and procedures.

The process begins by downloading the current customer profile from the database. If the event is configured to be processed by a workflow that has the profile merging action defined, or if the event is defined as an identification point in the customer journey, the system will use the defined "merge key" to load the profile data again necessary using this key instead of profile's ID. The merge key is usually an email address, credit card, etc.

If the system finds more than one profile with for example the same email address, it will merge the data from all profile records. The current profile and all other profiles that contain the merge key will be combined into a single profile.

If there are different values for the same field, for example, if one profile has the name "Bill" and another has the name "William", the system will consider the data to be in a "conflict state". The system will pick the last value and override the name, but will also save all available values in an "aux.conflict.name" field, for this example that would be ["Bill", "William"].

The combined profile will be given a new ID, and a new profile record will be created. All obsolete profiles will be deleted, and the events that were associated with the deleted profiles will be copied to the new merged profile.

The new profile ID will be saved by the javascript code on the device's local database. However, it's important to note that this does not mean that the reference to the current profile has been changed on all devices. It means that the system has a master profile of the customer with all the data collected from different devices but the devices themselves may not be updated with the new ID.

## Profile propagation

Consider the following example, a customer is using an online store with two different devices: a laptop and a mobile phone. Both devices have references to the customer's profile, but the profile ID is different on each device. On the laptop, the profile ID is 1, and on the mobile phone, the profile ID is 2.

At some point, the customer enters their email address into the online store using their laptop. A new merged profile is created and it has an ID of 3. The reference to this profile is saved in the browser on the laptop. However, the reference to the old profile is still stored on the mobile phone.

Next time when the customer uses their mobile phone to access the online store again, the system will use the old profile ID to identify the customer. But, instead of loading old profile, the system will download the new merged profile. This happens because Tracardi has the capability to recognize that an old profile ID no longer exists and has been merged with the new profile. Device will receive new profile ID that will be saved locally. 

This way, the information about the linked profile will be propagated to all devices. The customer will have the same profile ID on both devices and all the data will be updated and merged, this way the system can have a complete customer view and provide a better customer experience.
 
