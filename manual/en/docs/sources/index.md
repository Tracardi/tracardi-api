# Data resources

In order to kick start your new project with Tracardi needs a new resource. That resource defined in Tracardi will give
you an identifier which when attached to your track calls will start collecting data about your users. There are two
types of resources.

The resource that can emit events, e.g. web page, SMS gateways, received email, payload from kafka queue. This type of
resource sends data to Tracardi every time something happens.

The second type of resource is the resource that stores data, e.g. database. You have to query that resource for data.
It does not send data when the data is changed.

Tracardi can access both types of resources. For example, someone visits your page (first resource) Tracardi receives an
event with profile id then it queries the MySql database for additional data about the user (second resource).

Some resources may require user consent to collect data. A web page requires consent from the user to collect and store
user data.

## External services

Beside resources there are services that can consume or provide data. External services are very similar to databased
when they provide data. Tracardi can store those resources as well and use them to pass the data further.

## Credentials

Most of the resources need credentials that are used to connect to the resource. Credentials are attached to resource
and stored inside Tracardi. Resources are referenced inside workflow actions in order to read or save/send data.

### Credentials caching

Credentials are subject to caching. That means that after they are changed you will not see the change immediately but
after a certain number of seconds. Usually 60 seconds. Search for `SOURCE_TTL` for more information on cache settings. 
