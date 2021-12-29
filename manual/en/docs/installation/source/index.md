# Installation from source


## Software prerequisites

* Docker
* Python w wersji 3.8
* Pip
* Python Virtual Environment
* PyCharm
* Git

Install the above software and we're ready to start.

# Launching Elasticsearch

Open a terminal and enter: 

```
docker run -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:7.13.2

``` 

You have run a single instance of elasticsearch in the console. When you want to stop it, press CTRL + C 

!!! Tip

    If you want elasticsearch to run in the background, type: 
    `docker run -d -p 9200: 9200 -p 9300: 9300 -e "discovery.type = single-node" docker.elastic.co/elasticsearch/elasticsearch:7.13.2`

# Download the source code

Open a terminal and go to the directory where you want to keep the code. Enter:

```bash
git clone https://github.com/Tracardi/tracardi  #(1)
git clone https://github.com/Tracardi/tracardi-api #(2)
```

1. Clones tracardi repository. Code will be available in tracardi folder.
2.  Clones tracardi-api repository

# Create virtual environments 

Type:

```bash
cd tracardi-api
python3.8 -m venv venv  # (1)
cd ..
cd tracardi
python3.8 -m venv venv
```

1.   Installs virtual environment with python 3.8

!!! Tip  

    Before creating the virtual environment make sure you have version 3.8.x installed. Type `python --version` to see the typeon version.

# Install dependencies


=== "Linux"

    ```bash
    # Activates virtual environment (1)
    cd tracardi-api
    source venv/bin/activate
    
    # Installs dependencies
    pip install -r app/requirements.txt
    
    # Run code (2)
    USER_NAME=admin PASSWORD=admin uvicorn app.main:application --host 0.0.0.0 --port 8686
    ```

    1. Only tracardi-api is required to run the API. Tracardi library will be installed as dependency.
    2. Sets default username: password as admin: admin and runs Tracardi API on port 8686.

=== "Windows"

    ```bash
    cd tracardi-api
    venv\Scripts\activate
    
    // Installs dependencies
    pip install -r app/requirements.txt
    
    // Run code 
    USER_NAME=admin PASSWORD=admin uvicorn app.main:application --host 0.0.0.0 --port 8686
    ```

=== "Mac OS"

    ```bash
    // Activates virtual environment
    cd tracardi-api
    source venv/bin/activate
    
    // Installs dependencies
    pip install -r app/requirements.txt
    
    // Run code
    USER_NAME=admin PASSWORD=admin uvicorn app.main:application --host 0.0.0.0 --port 8686
    ```

# Test access to documentation

Visit http://0.0.0.0:8686/docs
