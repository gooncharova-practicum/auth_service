FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir -p /opt/tests
WORKDIR /opt/tests

COPY requirements.txt .
RUN  pip install -U pip setuptools && pip install --no-cache-dir -r requirements.txt

COPY . .