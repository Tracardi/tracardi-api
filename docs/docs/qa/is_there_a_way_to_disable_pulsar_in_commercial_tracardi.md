# Is there a way to disable Pulsar in Commercial Tracardi?

Yes, but it is not advisable. Disabling Pulsar will make Tracardi significantly less scalable, and all save operations
will be performed in the foreground rather than being pushed to the background worker.

# How to Disable Pulsar

To disable Pulsar, set `PULSAR_DISABLE` to `"yes"` or `"true"`. Using a Helm chart with this setting will stop the
background worker and execute all tasks with the current API event loop. This change will slow down all track requests.

# When to Disable Pulsar

It may be beneficial to disable Pulsar while debugging Tracardi or when there is minimal traffic on your website. In
such cases, to avoid maintaining the Pulsar instance, you can opt for a less performant Tracardi collector.
