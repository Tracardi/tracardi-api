FROM python:3.9-slim
MAINTAINER office@tracardi.com

RUN apt-get update && apt-get install -y --no-install-recommends git && apt-get purge -y --auto-remove && rm -rf /var/lib/apt/lists/*

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:/app:$PATH"

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

WORKDIR /app
ENV VARIABLE_NAME="application"

CMD ["uvicorn", "app.main:application", "--proxy-headers", "--host", "0.0.0.0",  "--port", "80", "--log-level", "warning"]
