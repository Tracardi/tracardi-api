# Outbound traffic

Tracardi can sync profiles with external systems. To do this use destinations.

Destination is a set of credentials that point to an external system where the profile data will be sent when if
changed. Destination require some resource, e.g. a API endpoint, queue service, etc. This is here you set all the
required information on the credentials and the location of the external system. Not all resources are available as
destinations.

Depending on the system version, the list of available destinations may change. The easiest way to check the available
ones is to go to the `resources/extensions` tab and filter out `type/destinations`. To use one of them you need to
install.

In version 0.7.2, the following resources were available for use as a destination.

* [Rabbitmq](../../resources/rabbitmq_resource.md)
* [Mautic](../../resources/mautic_resource.md)
* Remote API

When we have the resource to which we want to send data from the profile, go to the outbound traffic tab and select tab
destinations.

In the destination field you should see the resource. Then describe the destination in the __Destination description__
and fill the following fields:

* __Destination prerequisites__ - enter the condition that must be met for the profile synchronization to start with the
  external system. For example, `profile@data.contact.email.business exists` - it means that there must be a business e-mail in the profile to
  forward the data. The point is that the external system may require specific data to identify the user. You can leave
  this field blank that means, that regardless of the quality of the data, it will be sent to the destination system. To
  write a correct condition please read [how to use logic notation](../../notations/logic_notation.md)
* __Mapping__ - in this field we define the format of the data sent to the external system. The data is sent in the form
  of JSON. The data schema in Tracardi may differ from the expected schema in the external system. Here we can remap the
  data. Remapping is done by object
  templates. [Please read more on object templates](../../notations/object_template.md).
* __Destination setting__ - There may be additional destination settings required. Please fill them. For example an API
  call may require call method, or headers.

!!! Info

    In a commercial version __Destination is not synchronized right away after the first profile update__. The synchronisation is a postponed 
    process it means it will trigger after some time when the profile update process ends. For exmaple, when the 
    profile is updated every second for ten seconds the synchronisation will start after in about 20 seconds after the 
    last update. That means not earlier then 30 seconds from the first profile change. This is done on purpose 
    to not stress the remote system. 

