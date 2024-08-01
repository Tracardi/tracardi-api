# How to store interests in Tracardi

The "Add Interest" plugin in Tracardi is designed for adding and updating interests in a user's profile during workflow
processing.

In Tracardi, the "Add Interest" plugin can simplify the process of storing interests in user profiles. Here's how
you can use it within a workflow:

1. **Setup the Workflow**: Create a new workflow or edit an existing one where you want to incorporate the interest
   tracking. This workflow would typically be triggered by user actions that indicate their interests, such as viewing
   specific content or interacting with certain elements on your site.

2. **Add the Add Interest Plugin to Workflow**: Drag and drop the `Add Interest` plugin into your workflow. Connect this
   plugin to the appropriate part of your workflow, ensuring it's triggered by the relevant user actions.

3. **Configure the Plugin**: In the plugin configuration, specify the key under which the interest will be stored. This
   key will reside under the interests field in the profile. Assign a weight to the interest. This weight can quantify
   the level of interest, allowing for a more nuanced understanding of the user's preferences.

4. **Use Profile Update to store the interest**: Confirm the change to profile with `Profile Update` plugin.

You can use `Increase Interest` and `Decrease Interest` to update the interest weight.