#!/bin/bash

sudo docker service update up_config01
sudo docker service update up_shard01a
sudo docker service update up_shard02a
sudo docker service update up_shard03a
sleep 20
sudo docker service update up_mongo
