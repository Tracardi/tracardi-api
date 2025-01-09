# Build stage
FROM python:3.11-slim-bullseye AS builder

# Add build argument for GitHub token
ARG GITHUB_TOKEN
ENV VERSION="1.3.x"

RUN pip install --upgrade pip
# Install git
RUN apt-get update && apt-get install -y --no-install-recommends git build-essential && apt-get purge -y --auto-remove && rm -rf /var/lib/apt/lists/*

# Configure git to use token
RUN git config --global url."https://${GITHUB_TOKEN}@github.com/".insteadOf "https://github.com/"

# Clone your repository
WORKDIR /app
RUN git clone -b ${VERSION} https://github.com/Tracardi/tracardi-api  tracardi-api
RUN git clone -b ${VERSION} https://github.com/Tracardi/tracardi      tracardi
RUN git clone -b ${VERSION} https://github.com/Tracardi/deferpy       deferpy
RUN git clone -b ${VERSION} https://github.com/Tracardi/adapter       adapter
RUN git clone -b ${VERSION} https://github.com/Tracardi/documentation docs

RUN mkdir /system

RUN mkdir -p /system/docs         && cp -r /app/docs/docs                  /system
RUN mkdir -p /system/app          && cp -r /app/tracardi-api/app           /system
RUN mkdir -p /system/uix          && cp -r /app/tracardi-api/uix           /system
RUN mkdir -p /system/tracardi     && cp -r /app/tracardi/tracardi          /system
RUN mkdir -p /system/defer        && cp -r /app/deferpy/defer              /system
RUN mkdir -p /system/system       && cp -r /app/adapter/system             /system

# Remove test page
RUN rm -rf /system/app/tracker/index.html
RUN rm -rf /system/app/tracker/index.css

# Remove ee
RUN rm -rf /system/system/adapter/ee

WORKDIR /system

# Virtual env
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:/system:$PATH"

RUN pip install wheel
RUN pip --no-cache-dir --default-timeout=240 install -r tracardi/requirements.txt
RUN pip --no-cache-dir --default-timeout=240 install -r defer/requirements.txt
RUN pip --no-cache-dir --default-timeout=240 install -r app/requirements.txt

RUN pip list

# Final stage - token is not carried over to this stage
FROM python:3.11-slim-bullseye
MAINTAINER admin@tracardi.com

RUN pip install --upgrade pip

# Virtual env
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:/system:$PATH"

RUN pip install --upgrade pip

WORKDIR /system

COPY --from=builder /system .
COPY --from=builder $VIRTUAL_ENV $VIRTUAL_ENV

ENV VARIABLE_NAME="application"

# Set a default value for TAG_VERSION
ARG IMAGE_TAG=unknown
ENV IMAGE_TAG=${IMAGE_TAG}
ENV SERVER_LOGGING_LEVEL=warning
ENV PYTHONPATH="$VIRTUAL_ENV/bin:/system:$PYTHONPATH"
ENV PYTHONUNBUFFERED=1

CMD ["sh", "-c", "uvicorn app.main:application --proxy-headers --host 0.0.0.0 --port 80 --log-level $SERVER_LOGGING_LEVEL"]