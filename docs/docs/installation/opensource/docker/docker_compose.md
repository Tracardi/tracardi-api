# Open-source Tracardi with docker compose

## Installation

The easiest way to run TRACARDI is to run it as a :whale: docker container. Please install docker and docker-compose on your local machine 
then clone [tracardi/tracardi-api](https://github.com/Tracardi/tracardi-api.git)

```bash
git clone https://github.com/Tracardi/tracardi-api.git:<version>
```

Go to TRACARDI API folder, and run one line command:

```bash
cd tracardi-api
docker-compose up
```

This command will install all required services along with tracardi API and required workers. To test if the installation is correct visit http://localhost:8686.