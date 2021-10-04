FROM python:3.6

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR  /user_api

COPY . .

RUN apt-get update
RUN apt-get install -y default-libmysqlclient-dev
RUN pip install -r requirements.txt