#!/bin/bash
while ! nc -z config01:27017; do sleep 3; done
mongo --port 27020 < /scripts/init-shard03.js
