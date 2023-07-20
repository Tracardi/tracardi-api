# Profile merging and Identity resolution

## Profile Merging

Profile merging is the process of bringing together multiple customer profiles that belong to the same person but have
been stored separately for various reasons, like using different devices or email addresses. To create a complete
profile, a unique merging key is chosen to combine the data across the entire system. This merging key can be an email
address, credit card, or any other identifier that groups client profiles.

**Example:** Imagine a customer, John, uses his laptop with Firefox and gets profile ID 1. When he uses Google Chrome on
the same laptop, he gets profile ID 2. Then, when he uses his mobile phone, he gets profile ID 3. Although all these
profiles represent John, they have different data. For instance, profile ID 1 may have purchase data but not his name,
which is saved in profile ID 2. By merging these profiles, we can have a complete understanding of John as a customer.

## Identity Resolution

Identity resolution is a broader term used to link various pieces of data about an individual or entity to create a
comprehensive and accurate view. In a customer data platform (CDP), identity resolution helps connect data from
different sources, like website interactions and email campaigns, to form a unified customer profile.

## Merging Process

Merging customer profiles is a complex process that involves following rules and procedures. It starts by retrieving the
current customer profile from the database. If the event is handled by a workflow with the profile merging action or is
marked as an identification point in the customer journey, the system uses the defined "merge key" (like an email
address) to load the profile data instead of the profile's ID.

If the system finds multiple profiles with the same merge key, it merges the data from all these profiles into one. In
case of conflicting data, like different names, the system resolves the conflict by picking the last value and saving
other values in an "aux.conflict.name" field, like ["Bill", "William"].

The merged profile receives a new ID, and a new profile record is created. Obsolete profiles are deleted, and the events
associated with the deleted profiles are copied to the new merged profile.

The new profile ID is saved locally on the device's database using JavaScript. However, it's important to note that not
all devices may update their reference to the current profile with the new ID immediately.

## Profile Propagation

Consider this example: A customer uses an online store with a laptop and a mobile phone, and each device has a different
profile ID. The laptop has profile ID 1, and the mobile phone has profile ID 2.

At some point, the customer enters their email address on the laptop, creating a new merged profile with ID 3. The
laptop's browser saves a reference to this new profile. However, the mobile phone still stores the reference to the old
profile.

The next time the customer uses their mobile phone to access the online store, the system uses the old profile ID to
identify them. But instead of loading the old profile, the system recognizes that the old profile ID has been merged
with a new profile. The mobile phone receives the new profile ID (3) and saves it locally.

This way, the linked profile information propagates to all devices, and the customer will have the same updated profile
ID on both the laptop and the mobile phone. This provides a complete customer view and improves the overall customer
experience.

!!! Note

    It is **very important** to synchronize `profile.id` returned in response with the profile ID saved on a client side.
    If the profile in the response is different from the one sent, it means the client should update its `profile.id` 
    and send the new one with the next call. Missing this step may cause the `profile.id` to be recreated with each 
    call to the /track API, potentially causing issues with the customer's profile.