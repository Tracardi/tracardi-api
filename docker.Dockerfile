FROM tiangolo/uvicorn-gunicorn-fastapi:python3.10
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

# Prepare in CD from REPO tracardi/doumentation
# +:docs => docs

COPY docs app/docs/

# Remove after 30-08-2024
# Commented bo nie bedziemy robic dokumentacji w kazdym dokerze
#WORKDIR /docs
#
### Install docs dependencies
#RUN pip --default-timeout=240 install -r requirements.txt
#
## Install manual
#
#RUN mkdocs build
#RUN mv site app
#RUN mv docs app

# Start up

WORKDIR /app
ENV VARIABLE_NAME="application"

# Set a default value for TAG_VERSION
ARG IMAGE_TAG=unknown
ENV IMAGE_TAG=${IMAGE_TAG}

CMD ["uvicorn", "app.main:application", "--proxy-headers", "--host", "0.0.0.0",  "--port", "80", "--log-level", "info"]
