FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11
MAINTAINER office@tracardi.com

RUN apt-get update && apt-get install -y --no-install-recommends git && apt-get purge -y --auto-remove && rm -rf /var/lib/apt/lists/*
#RUN sudo apt install python3.11-dev

# Virtual env
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV

ENV PATH="$VIRTUAL_ENV/bin:/src:$PATH"

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

# Prepare in CD from REPO tracardi/deferpy
# +:defer => defer
COPY defer defer/

# Prepare in CD from REPO tracardi/doumentation
# +:docs => docs
COPY docs docs/

RUN pip --default-timeout=240 install -r app/requirements.txt
RUN pip --default-timeout=240 install -r defer/requirements.txt

RUN pwd
RUN ls -al

# Start up

ENV VARIABLE_NAME="application"

# Set a default value for TAG_VERSION
ARG IMAGE_TAG=unknown
ENV IMAGE_TAG=${IMAGE_TAG}
ENV SERVER_LOGGING_LEVEL=info
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH="$VIRTUAL_ENV/bin:/src:$PYTHONPATH"

#CMD ["uvicorn", "app.main:application", "--proxy-headers", "--host", "0.0.0.0",  "--port", "80", "--log-level", "${SERVER_LOGGING_LEVEL}"]
CMD ["sh", "-c", "uvicorn app.main:application --proxy-headers --host 0.0.0.0 --port 80 --log-level $SERVER_LOGGING_LEVEL"]
