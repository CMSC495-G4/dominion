FROM python:3

RUN apt-get update \
 && apt-get upgrade \
 && apt-get install \
    apache2 \
    apache2-dev

RUN mkdir -p /code \
 && chown -R code apache:apache

WORKDIR /code

COPY Pipfile .

RUN pip install --upgrade pip \
 && pip install \
    mod_wsgi \
    pipenv \
 && pipenv install

CMD pipenv shell