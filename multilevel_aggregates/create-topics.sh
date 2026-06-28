#!/bin/bash -e
docker exec `docker ps --format '{{.Names}}' --filter ancestor=docker.io/bitnami/kafka:latest` kafka-topics.sh --bootstrap-server $1 --topic ac_sub --create --partitions 3 --replication-factor 1 &
docker exec `docker ps --format '{{.Names}}' --filter ancestor=docker.io/bitnami/kafka:latest` kafka-topics.sh --bootstrap-server $1 --topic ac_pub --create --partitions 3 --replication-factor 1 &
docker exec `docker ps --format '{{.Names}}' --filter ancestor=docker.io/bitnami/kafka:latest` kafka-topics.sh --bootstrap-server $1 --topic aqi_sub --create --partitions 3 --replication-factor 1 &
docker exec `docker ps --format '{{.Names}}' --filter ancestor=docker.io/bitnami/kafka:latest` kafka-topics.sh --bootstrap-server $1 --topic temperature_sub --create --partitions 3 --replication-factor 1 &
docker exec `docker ps --format '{{.Names}}' --filter ancestor=docker.io/bitnami/kafka:latest` kafka-topics.sh --bootstrap-server $1 --topic occupancy_sub --create --partitions 3 --replication-factor 1 &
docker exec `docker ps --format '{{.Names}}' --filter ancestor=docker.io/bitnami/kafka:latest` kafka-topics.sh --bootstrap-server $1 --topic purifier_sub --create --partitions 3 --replication-factor 1 &
docker exec `docker ps --format '{{.Names}}' --filter ancestor=docker.io/bitnami/kafka:latest` kafka-topics.sh --bootstrap-server $1 --topic purifier_pub --create --partitions 3 --replication-factor 1 &
wait
