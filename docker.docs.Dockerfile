FROM python:3.9
MAINTAINER office@tracardi.com

RUN apt-get update
RUN apt-get install -y git

# update pip
RUN /usr/local/bin/python -m pip install --upgrade pip

## Copy manual
COPY docs docs/
COPY mkdocs.yml /

## Install dependencies
RUN pip install wheel
RUN pip --default-timeout=180 install -r docs/requirements.txt
WORKDIR /
RUN mkdocs build

EXPOSE 8585

CMD ["mkdocs", "serve"]
