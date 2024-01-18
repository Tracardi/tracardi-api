# How can Tracardi be installed as a Docker container?

- Tracardi can be easily installed as a Docker container by following the provided instructions.

# What are the dependencies for running Tracardi?

- Tracardi requires Elasticsearch, Redis, Tracardi API, and Tracardi GUI to run. Docker containers need to be started
  for each of these services.

# How can I start the Elasticsearch database for Tracardi?

- The Elasticsearch database for Tracardi can be started by pulling and running the Elasticsearch single-node Docker
  image with the provided command.

# How can I start the Redis instance for Tracardi?

- The Redis instance for Tracardi can be started by running the Redis Docker container with the provided command.

# How can I start the Tracardi API?

- The Tracardi API can be started by pulling and running the Tracardi API Docker image with the provided command. Make
  sure to set the necessary environment variables, such as the Elastic host and Redis host.

# How can I connect Tracardi to Elasticsearch via SSL?

- If you have an Elasticsearch instance and want to connect to it via HTTPS, you can use the provided command with the
  necessary environment variables set accordingly.

# How can I start the Tracardi GUI?

- The Tracardi GUI can be started by pulling and running the Tracardi GUI Docker image with the provided command.

# How can I run the import worker in Tracardi?

- To run the import worker in Tracardi, you can use the provided command to start the worker Docker container. Make sure
  to set the Redis host accordingly.

# How can I access the Tracardi Graphical User Interface (GUI)?

- The Tracardi GUI can be accessed by visiting the provided URL and following the instructions for Tracardi setup. Make
  sure to specify the Tracardi API URL correctly.

# Where can I find the system documentation for Tracardi?

- The system documentation for Tracardi can be accessed by visiting the provided URL. Make sure the documentation Docker
  is started.

# Where can I find the API documentation for Tracardi?

- The API documentation for Tracardi can be accessed by visiting the provided URL.

# How can I specify a specific version when installing Tracardi?

- To install a specific version of Tracardi, you can add a version tag to the Docker image name in the command, such
  as `tracardi/tracardi-api:<version>` or `tracardi/tracardi-gui:<version>`.

# What is the purpose of running multiple instances of Elasticsearch in Tracardi?

- Running multiple instances of Elasticsearch in Tracardi is not a production solution but can be done for testing
  purposes. For production use, it is recommended to run an Elasticsearch cluster. Documentation is available for
  connecting Tracardi to an Elasticsearch cluster.

# How can I troubleshoot issues with Tracardi installation?

- For troubleshooting solutions during Tracardi installation, you can refer to the provided documentation section on
  troubleshooting.

# Can I run Tracardi without starting the Redis instance?

- No.

# Can I use Tracardi with an existing Elasticsearch instance?

- Yes, you can connect Tracardi to an existing Elasticsearch instance. Documentation is available for connecting
  Tracardi to Elasticsearch via SSL.

# How can I access the Tracardi API documentation?

- The Tracardi API documentation can be accessed by visiting the provided URL.

# How can I access the local copy of the Tracardi documentation?

- The local copy of the Tracardi documentation can be accessed by visiting the provided URL. Make sure the documentation
  Docker is started.

# Can I access Tracardi API and GUI from different IP addresses?

- Yes, you can access the Tracardi API and GUI from different IP addresses by replacing "localhost" with the appropriate
  IP in the configuration.

# Can I specify a different version for the Tracardi worker?

- Yes, you can specify a different version for the Tracardi worker by adding a version tag to the Docker image name in
  the command, such as `tracardi/update-worker:<version>`. Make sure to keep the worker version the same as the Tracardi
  API version.

# What are the software prerequisites for installing Tracardi from source?

The software prerequisites for installing Tracardi from source are:

- Docker
- Python version 3.9 or 3.10 (for version 0.8.1+)
- Pip
- Python Virtual Environment
- PyCharm
- Git

# What are the options for launching Elasticsearch on Ubuntu?

There are two options for launching Elasticsearch on Ubuntu:

1. Installing Elasticsearch as a service
2. Installing Elasticsearch as a Docker container

# How can I install Elasticsearch as a service on Ubuntu?

To install Elasticsearch as a service on Ubuntu, follow these steps:

- Import the Elasticsearch public GPG key using cURL and add the Elastic package source list.
- Update the package lists and install Elasticsearch using APT.

# How can I install Elasticsearch as a Docker container on Ubuntu?

To install Elasticsearch as a Docker container on Ubuntu, use the following command:

```
docker run -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:7.13.2
```

# How do I download the Tracardi source code?

To download the Tracardi source code, use the following commands:

```
git clone https://github.com/Tracardi/tracardi
git clone https://github.com/Tracardi/tracardi-api
```

# How do I create virtual environments for Tracardi source?

To create virtual environments for Tracardi, follow these steps:

- Navigate to the respective directory (`tracardi-api` or `tracardi`).
- Use the `python3.10 -m venv venv` command to create a virtual environment.

# How do I install the dependencies for Tracardi when installing form source?

The installation steps for dependencies vary depending on the operating system:

### Linux

```
cd tracardi-api
source venv/bin/activate
pip3 install wheel
pip install -r app/requirements.txt
```

### Windows

```
cd tracardi-api
venv\Scripts\activate
pip install -r app/requirements.txt
```

### Mac OS

```
cd tracardi-api
source venv/bin/activate
pip install -r app/requirements.txt
```

# How can I test access to the Tracardi documentation?

To test access to the Tracardi documentation, visit http://0.0.0.0:8686/docs.