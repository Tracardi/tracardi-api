# How to enable system events in helm chart?

To enable system events in Tracardi, you need to adjust the configuration settings in the `values.yaml` file. Here’s how
you can do it:

1. **Locate the `values.yaml` file**: This file contains the configuration settings for Tracardi. If you don't already
   have a custom `values.yaml` file, you will need to create one by copying the default settings and then making the
   necessary modifications.

2. **Modify the configuration to enable system events**: In the `values.yaml` file, find the `config` section and set
   the `systemEvents` field to `"yes"`.

Here is an example of what the relevant part of your `values.yaml` file should look like:

```yaml title="Part of values.yaml file"  hl_lines="5"
config:
  multiTenant:
    multi: "yes"  # Enable multi-tenancy if needed
  primaryId: "emm-"  # Set the primary ID prefix if needed
  systemEvents: "yes"  # Enable system events
  enableVisitEnded: "no"  # Enable visit ended events if needed
  visit:
    close: 1800  # Set visit close time to 1800 seconds (30 minutes)
```

3. **Deploy the changes**: After modifying the `values.yaml` file, deploy the changes to your Tracardi instance. The
   exact method of deployment will depend on your environment. For example, if you are using Helm, you can use the
   following command to apply the changes:

```bash
helm upgrade --install tracardi ./tracardi -f values.yaml
```

By setting `systemEvents` to `"yes"`, you enable the system events in Tracardi, allowing the platform to generate and
handle internal events that provide insights into various operations and activities within the system.
