FROM python:3.8.6-buster

LABEL project="telephone_numbers"

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
#ENV ENVIRONMENT "docker"

WORKDIR /code

COPY Pipfile Pipfile.lock /code/
RUN pip install pipenv  && pipenv install --system --ignore-pipfile


COPY telephone_numbers /code/

