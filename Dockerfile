FROM python:3.8-slim-buster
ENV PYTHONUNBUFFERED=1
RUN apt-get update && apt-get -y install libpq-dev gcc
WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
