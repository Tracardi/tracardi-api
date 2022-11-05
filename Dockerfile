FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9
MAINTAINER office@tracardi.com

RUN apt-get update
RUN apt-get install -y git

# update pip
RUN /usr/local/bin/python3 -m pip install --upgrade pip

# set the working directory in the container
RUN mkdir app/
WORKDIR /app

## Install dependencies
COPY app/requirements.txt .
RUN pip install wheel
RUN pip --default-timeout=240 install -r requirements.txt

RUN pip show tracardi
RUN pip list


## Copy application
COPY app app/
COPY uix uix/

# Remove test page

RUN rm -rf app/tracker/index.html
RUN rm -rf app/tracker/index.css

WORKDIR /

## Copy manual
COPY docs docs/
COPY mkdocs.yml /

## Install docs dependencies
RUN pip --default-timeout=240 install -r docs/requirements.txt

# Install manual

RUN mkdocs build
RUN mv site app
RUN mv docs app

# Start up

WORKDIR /app
ENV VARIABLE_NAME="application"
