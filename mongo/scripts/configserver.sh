#!/bin/bash
dockerize -wait tcp://config02:27017 -timeout 20s
dockerize -wait tcp://config03:27017 -timeout 20s

mongo --port 27017 < /scripts/init-configserver.js
