#!/bin/bash -e
docker exec `docker ps --format '{{.Names}}' --filter ancestor=docker.io/bitnami/kafka:latest` kafka-topics.sh --bootstrap-server $1 --topic arc_cell_sub --create --partitions 3 --replication-factor 1 &
docker exec `docker ps --format '{{.Names}}' --filter ancestor=docker.io/bitnami/kafka:latest` kafka-topics.sh --bootstrap-server $1 --topic arc_cell_pub --create --partitions 3 --replication-factor 1 &
wait
