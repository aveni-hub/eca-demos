#!/bin/bash
set -euo pipefail

BOOTSTRAP_SERVER=${1:-localhost:9092}
COMPOSE_FILE_PATH=${COMPOSE_FILE_PATH:-docker-compose-main.yaml}
KAFKA_TOPICS_BIN=${KAFKA_TOPICS_BIN:-/opt/kafka/bin/kafka-topics.sh}
BROKER_CONTAINER=${BROKER_CONTAINER:-$(docker compose -f "$COMPOSE_FILE_PATH" ps -q kafka)}

if [ -z "$BROKER_CONTAINER" ]; then
    echo "Could not resolve the Kafka container from $COMPOSE_FILE_PATH." >&2
    echo "Start the compose stack first, or set BROKER_CONTAINER explicitly." >&2
    exit 1
fi

create_topic() {
    docker exec "$BROKER_CONTAINER" "$KAFKA_TOPICS_BIN" \
        --bootstrap-server "$BOOTSTRAP_SERVER" \
        --topic "$1" \
        --create \
        --if-not-exists \
        --partitions 3 \
        --replication-factor 1
}

create_topic ac_sub &
create_topic ac_pub &
create_topic aqi_sub &
create_topic temperature_sub &
create_topic occupancy_sub &
create_topic purifier_sub &
create_topic purifier_pub &
create_topic aggregate001 &
create_topic temperature &
create_topic occupancy &
create_topic air_conditioner &
create_topic air_quality_index &
create_topic purifier &
wait
