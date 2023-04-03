# How to use own profile id?

To set your own profile ID in Tracardi, there are two ways to do it. The first way requires a commercial bridge, while
the second way is an open source method. The open source method involves passing your profile ID in properties, copying
it to profile IDs in a workflow, and storing it in the profile's "ids" property. This allows you to use your own ID to
get the profile. It's important to note that if you expose the collector to the internet, you must ensure that your
profile ID is in the form of a UUID4 or another hard-to-guess ID to avoid messing up data.