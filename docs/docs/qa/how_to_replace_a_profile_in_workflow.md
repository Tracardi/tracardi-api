# How to Replace a Profile in Workflow?

Sometimes, it may be necessary to replace a profile with a different profile based on certain data from the event
properties. This documentation will walk through how to do this using a workflow and looking for a profile based on a
specific identifier, such as an email address. By following the instructions below, you can easily replace a profile and
ensure that the correct information is being used in the workflow.

* Create a workflow with a start and end node
* Add a "Load Profile by" node and connect it to the start node
* Select the field (e.g., email) that you would like to use to identify the profile
* Send the email in the event properties
* Add an "Event Properties" node and connect it to the "Load Profile by" node for debugging purposes
* Run the workflow
* Check the state of the profile to ensure it was successfully loaded
* If the email is misspelled, there will be an error indicating that no record was found
* Consider what to do with events that do not have a profile (e.g., discard the event or keep it for further analysis)