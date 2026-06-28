# Operator-Binding Abstractions Demo

This lane is the curated, top-down abstraction demo for `eca_demos`.

It seeds:

- base definition ESS states for a tiny `3x3` board program
- two operator abstractions (`rotate_180`, `translate_right_1`)
- one sequence abstraction that chains those operators

Then it streams only `A` and runs reasoning to show the seeded program is selected and executed through the normal
explore -> goal -> subgoal flow.

## Story

The source stream exposes one deterministic state:

- `A`: a single active cell at the top-right

The seeded program should make the reasoning loop produce:

- `B`: `A` rotated `180` degrees to the bottom-left
- `C`: `B` translated right by `1` to the bottom-center

The seeded abstraction program is:

`prog1 = [rotate_180(A -> B), translate_right_1(B -> C)]`, with `prog1` preferred over the leaf abstractions during exploration.

## Files

- `data/board_states.jsonl`: the tiny board-state stream used by the demo
- `seed/programmed_story.json`: declarative seed payload describing the curated abstraction definitions
- `configs/`: generated `mono`, `server`, source-twin, and cortex configs
- `create-topics.sh`: creates the Kafka topic used by the source streamer
- `producer.py`: streams the tiny board-state dataset into Kafka
- `run_demo.py`: thin wrapper around `producer.py`
- `api_seed.py`: seeds definition ESS plus operator/sequence abstractions through the server API
- `api_inspect.py`: inspects abstractions, attention sequence, goals, and goal stack through the server API

## Run

```bash
cd /Users/ogbanugot/Workspace/aveni
python eca_demos/operator_binding_abstractions/config.py
docker compose -f eca_demos/smart_iot/docker-compose-main.yaml up -d
bash eca_demos/operator_binding_abstractions/create-topics.sh localhost:9092
```

Start the existing mono binary in one terminal:

```bash
cd /Users/ogbanugot/Workspace/aveni/avenieca
export LIBRARY_PATH=/opt/homebrew/opt/openblas/lib:${LIBRARY_PATH}
./target/release/avenieca mono --config ../eca_demos/operator_binding_abstractions/configs/mono.json
```

Start the server binary in a second terminal:

```bash
cd /Users/ogbanugot/Workspace/aveni/avenieca
export LIBRARY_PATH=/opt/homebrew/opt/openblas/lib:${LIBRARY_PATH}
./target/release/server --config ../eca_demos/operator_binding_abstractions/configs/server.json
```

Seed the curated abstractions through the API:

```bash
cd /Users/ogbanugot/Workspace/aveni/eca_demos/operator_binding_abstractions
python api_seed.py
```

Stream the source state from a third terminal:

```bash
cd /Users/ogbanugot/Workspace/aveni/eca_demos/operator_binding_abstractions
python run_demo.py
sleep 3
python api_inspect.py
```

What should be manual vs automatic now:

- manual: definition ESS + abstraction seeding
- automatic: explore selects `prog1`, root goal creation, subgoal push, operator-stage execution, and attention change from `A -> B -> C`

This now follows the same runtime shape as `smart_iot`, with API-side seeding and inspection through the existing server binary:

- Postgres on `localhost:5432`
- Qdrant on `http://localhost:6334`
- Kafka on `127.0.0.1:9092`
- Server API on `http://localhost:2580/v1`
- Default API login: `default@email.com` / `admin`
