Tracardi microservice plugin is a new way to extend Tracardi without system upgrade. 
Each microservice can deliver a set of new plugins that you can easily plug and use. 
The main benefit of using Tracardi microservices is access to continuously growing set of services 
and zero maintenance cost.

# Tracardi Microservice Credentials

To use the Tracardi microservice plugin you will need to provide an API KEY.

## Where to get Microservice's API key

Microservice is usually a new docker that you start on your server. Tracardi microservices require you to set 
API_KEY environment variable. It must be at least 32 char long. And must be a random value hard to guess.

Please paste this value to API key input and click __get secret__. Your APIKEY will be replaced by token
that will allow you to access the server microservices. 

# Microservice setup

* Type the microservice URL to Type microservice URL Input.
* Type the API KEY and click __get secret__. If the API KEY is correct you will see the green lock.
* Select on of the available services that are installed on the microservice server.
* Depending on the selected service you may see additional form to fill with the credentials that are required for
  the service to work. For example a service that integrates with Trello will require the Trello credentials.  
* If the developer provided the documentation for the microservice you should see the manual with the tips how to 
  configure the selected service. 


# Microservice plugins

Each microservice installs plugins that will connect to the microservice and run the configured action. Plugins can be 
found in the workflow editor. 

