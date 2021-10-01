FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8
MAINTAINER office@tracardi.com

RUN apt-get update
RUN apt-get install -y git

# update pip
RUN /usr/local/bin/python -m pip install --upgrade pip

# set the working directory in the container
RUN mkdir app/
WORKDIR /app

## Install dependencies
COPY app/requirements.txt .
RUN pip install -r requirements.txt

RUN pip show tracardi

## Copy application
COPY app app/

## Copy manual
COPY manual manual/
## Install dependencies
RUN pip install -r manual/requirements.txt
WORKDIR /app/manual/en
RUN mkdocs build

ENV VARIABLE_NAME="application"
