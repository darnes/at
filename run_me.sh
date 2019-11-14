#!/usr/bin/env bash

# building and packaging
PACKAGE_IMAGE_NAME="dshw-package"


docker build -t ${PACKAGE_IMAGE_NAME} ./
DOCKER_ID=$(docker create ${PACKAGE_IMAGE_NAME})
docker cp ${DOCKER_ID}:/home/at/dshw/dist/. ./infra/target/dist/
docker rm ${DOCKER_ID}
docker image rm ${PACKAGE_IMAGE_NAME} -f

# kicking of infra
docker-compose build
docker-compose up
