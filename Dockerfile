FROM python:3.9.10

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt update
RUN apt install -y postgresql

COPY . /app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt