#!/bin/bash
dockerize -wait tcp://config01:27017 -timeout 20s
dockerize -wait tcp://shard01a:27018 -timeout 20s
dockerize -wait tcp://shard02a:27019 -timeout 20s
dockerize -wait tcp://shard03a:27020 -timeout 20s

mongo < /scripts/init-router.js
