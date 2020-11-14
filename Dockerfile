FROM python:3.8.6-buster

LABEL project="telephone_numbers"

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
#ENV ENVIRONMENT "docker"

WORKDIR /code

COPY Pipfile Pipfile.lock /code/
RUN pip install pipenv  && pipenv install --system --ignore-pipfile


COPY telephone_numbers /code/



# This one works
#FROM python:3.8.6
#
#LABEL project='telephone_numbers'
#
#ENV PYTHONDONTWRITEBYTECODE 1
#ENV PYTHONUNBUFFERED 1
#
#WORKDIR /code
#
#COPY Pipfile /code/
#RUN pip install pipenv && pipenv install
#
#COPY telephone_numbers /code/
