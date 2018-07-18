#!/bin/bash
dockerize -wait tcp://config01:27017 -timeout 20s
mongo --port 27020 < /scripts/init-shard03.js
