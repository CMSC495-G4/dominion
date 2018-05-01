#!/bin/bash -ex

cp -R /code/src /deploy

pushd /deploy

python3.6 manage.py collectstatic --noinput

chown -R apache:apache /deploy

python3.6 manage.py runserver 0:80
