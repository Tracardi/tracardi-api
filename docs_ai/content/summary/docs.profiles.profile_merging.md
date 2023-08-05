Profile merging and identity resolution are two important processes used in customer data platforms (CDPs) to create a
complete and accurate picture of a customer. Profile merging is the process of combining multiple customer profiles that
belong to the same person, but have been saved as separate records. This is done by selecting a merging key, such as an
email address, credit card, or any other global identifier that can be used to group client profiles. Identity
resolution is a broader term and is the process of linking multiple pieces of data about a single individual or entity,
in order to create a complete and accurate picture of that individual or entity.

The merging process begins by downloading the current customer profile from the database. If the system finds more than
one profile with the same merge key, it will merge the data from all profile records. The current profile and all other
profiles that contain the merge key will be combined into a single profile. If there are different values for the same
field, the system will consider the data to be in a "conflict state" and will pick the last value and override the name,
but will also save all available values in an "aux.conflict.name" field. The combined profile will be given a new ID,
and a new profile record will be created. All obsolete profiles will be deleted, and the events that were associated
with the deleted profiles will be copied to the new merged profile.

Profile propagation is also an important part of the merging process. This is the process of updating the reference to
the new merged profile on all devices. The customer will have the same profile ID on both devices and all the data will
be updated and merged, this way the system can have a complete customer view and provide a better customer experience.