#!/bin/bash
while ! nc -z config01:27017; do sleep 3; done
while ! nc -z shard01a:27018; do sleep 3; done
while ! nc -z shard02a:27019; do sleep 3; done
while ! nc -z shard03a:27020; do sleep 3; done
mongo < /scripts/init-router.js
