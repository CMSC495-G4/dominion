#!/bin/bash

cd ..

docker build -t dominion -f deploy/Dockerfile .

docker rm -f dominion-app

docker run -dp 80:80 -v "$PWD:/code" --name dominion-app dominion