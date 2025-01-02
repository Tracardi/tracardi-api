FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11
MAINTAINER office@tracardi.com

RUN apt-get update
RUN apt-get install -y git
#RUN sudo apt install python3.11-dev

# update pip
RUN /usr/local/bin/python3 -m pip install --upgrade pip
RUN pip install wheel

# set the working directory in the container
RUN mkdir src/
WORKDIR /src

## Copy application
COPY app app/
# Remove test page

RUN rm -rf app/tracker/index.html
RUN rm -rf app/tracker/index.css

COPY uix uix/

RUN pip --default-timeout=240 install -r app/requirements.txt

# Prepare in CD from REPO tracardi/deferpy
# +:defer => defer
COPY defer defer/

# Prepare in CD from REPO tracardi/doumentation
# +:docs => docs
COPY docs docs/

# Start up

ENV VARIABLE_NAME="application"

# Set a default value for TAG_VERSION
ARG IMAGE_TAG=unknown
ENV IMAGE_TAG=${IMAGE_TAG}
ENV SERVER_LOGGING_LEVEL=info

#CMD ["uvicorn", "app.main:application", "--proxy-headers", "--host", "0.0.0.0",  "--port", "80", "--log-level", "${SERVER_LOGGING_LEVEL}"]
CMD ["sh", "-c", "uvicorn app.main:application --proxy-headers --host 0.0.0.0 --port 80 --log-level $SERVER_LOGGING_LEVEL"]
