#!/bin/bash

pushd ..

docker build -t dominion -f deploy/Dockerfile .

docker rm -f dominion-app

docker run -dp 8000:80 -v "$pwd:/code" --name dominion-app dominion