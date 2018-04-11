#!/bin/bash -ex

cp -R /code/src /deploy

pushd /deploy

python3.6 manage.py collectstatic --noinput

chown -R apache:apache /deploy


mod_wsgi-express start-server dominion/wsgi.py \
  --user apache \
  --group apache \
  --port 80 \
  --reload-on-changes \
  --url-alias /static static/ ## need trailing slash for directory