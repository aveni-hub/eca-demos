#!/bin/bash
set -euo pipefail

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
BOOTSTRAP_SERVER=${1:-localhost:9092}
COMPOSE_FILE_PATH=${COMPOSE_FILE_PATH:-"$SCRIPT_DIR/../smart_iot/docker-compose-main.yaml"}
KAFKA_TOPICS_BIN=${KAFKA_TOPICS_BIN:-/opt/kafka/bin/kafka-topics.sh}
BROKER_CONTAINER=${BROKER_CONTAINER:-$(docker compose -f "$COMPOSE_FILE_PATH" ps -q kafka)}

if [ -z "$BROKER_CONTAINER" ]; then
    echo "Could not resolve the Kafka container from $COMPOSE_FILE_PATH." >&2
    echo "Start the compose stack first, or set BROKER_CONTAINER explicitly." >&2
    exit 1
fi

docker exec "$BROKER_CONTAINER" "$KAFKA_TOPICS_BIN" \
    --bootstrap-server "$BOOTSTRAP_SERVER" \
    --topic operator_binding_source_sub \
    --create \
    --if-not-exists \
    --partitions 3 \
    --replication-factor 1

docker exec "$BROKER_CONTAINER" "$KAFKA_TOPICS_BIN" \
    --bootstrap-server "$BOOTSTRAP_SERVER" \
    --topic opbind_pp_agent394fx313 \
    --create \
    --if-not-exists \
    --partitions 3 \
    --replication-factor 1

docker exec "$BROKER_CONTAINER" "$KAFKA_TOPICS_BIN" \
    --bootstrap-server "$BOOTSTRAP_SERVER" \
    --topic opbind_pp_reasoning495dj583 \
    --create \
    --if-not-exists \
    --partitions 3 \
    --replication-factor 1

docker exec "$BROKER_CONTAINER" "$KAFKA_TOPICS_BIN" \
    --bootstrap-server "$BOOTSTRAP_SERVER" \
    --topic opbind_pag_goal294ee212 \
    --create \
    --if-not-exists \
    --partitions 3 \
    --replication-factor 1
