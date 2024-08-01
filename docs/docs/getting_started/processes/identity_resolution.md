# Identity Resolution

Identity resolution is a process that combines [Tracking](tracking.md), [Identification](identification.md)
and [Merging Profiles](merging.md).

## Data Collection

Data collection involves gathering events and interactions from various devices. One set of events may be collected on
one device, and another on different devices, resulting in different Profile IDs for the same user. Data collection
itself is not responsible for merging these profiles.

## Identity Resolution Processes

Identity resolution includes several key processes:

- **[Tracking](tracking.md)**: The process of maintaining a consistent single Profile ID across all customer
  interactions on a single device. It is the responsibility of the device/client to keep the Profile ID unchanged and
  this is a process on the device.

- **[Merging Profiles](merging.md)**: Tracardi merges the existing profiles collected on different devices or from
  different channels into a single unified profile. This is a server process that returns the new Profile ID to the
  client.

- **[Identification](identification.md)**: The resulting unified profile may retain multiple profile IDs to identify the
  same profile created on different devices or browsers. This is a server process that ensures that all historical
  Profile IDs are stored in the system.

!!! Note

    The profile ID sent in the tracking payload may be different in the Tracardi response. For more details, 
    see [why my profile ID in the response from Tracardi is different from the one I have sent](merging.md).