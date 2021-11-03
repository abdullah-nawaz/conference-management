FROM python:3.6

ADD . /conference-management
WORKDIR /conference-management

# Install pre-requisites
RUN apt-get update
RUN apt-get install -y \
    build-essential \
    default-libmysqlclient-dev \
    python3-dev

RUN pip3 install --upgrade pip
RUN pip3 install -r /conference-management/requirements.txt
