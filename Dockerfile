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
RUN pip --default-timeout=180 install -r requirements.txt

RUN pip show tracardi
RUN pip list


## Copy application
COPY app app/
COPY uix uix/

## Copy manual
COPY manual manual/

## Install dependencies
RUN pip --default-timeout=180 install -r manual/requirements.txt
WORKDIR /app/manual/en
RUN mkdocs build

ENV VARIABLE_NAME="application"
