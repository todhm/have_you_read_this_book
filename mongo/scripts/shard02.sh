#!/bin/bash
dockerize -wait tcp://config01:27017 -timeout 20s
mongo --port 27019 < /scripts/init-shard02.js
