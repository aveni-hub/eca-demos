# Auto-Abstraction Creation Demo

This lane is the bottom-up abstraction demo for `eca_demos`.

It starts with no hand-authored abstractions, streams repeated `A -> B -> C` board transitions,
and then separates the run into two explicit phases:

1. experience accumulation
2. learning and replay

## Story

The raw stream repeats a tiny transform chain on a `3x3` board:

- `A`: top-right cell active
- `B`: `A` rotated `180` degrees to the bottom-left
- `C`: `B` translated right by `1` to the bottom-center

The learning pass shows:

- learned operator-bearing abstractions from the repeated transitions
- a learned sequence abstraction from the repeated transform chain
- a replay-time recurrent pattern abstraction when the learned context is explored again

## Files

- `data/repeated_windows.jsonl`: repeated `A -> B -> C` experience stream
- `configs/`: generated `mono`, `server`, source-twin, and cortex configs
- `create-topics.sh`: creates the Kafka topic used by the source streamer
- `producer.py`: streams the repeated experience dataset into Kafka
- `run_demo.py`: thin wrapper around `producer.py`
- `api_stage_learning.py`: stages PAG attention into the `core-aa` attention stream so the learning pass is explicit and observable
- `api_inspect.py`: inspects learned abstractions, attention sequence, and goal stack through the server API

## Run

```bash
cd /Users/ogbanugot/Workspace/aveni
python eca_demos/auto_abstraction_creation/config.py
docker compose -f eca_demos/smart_iot/docker-compose-main.yaml up -d
bash eca_demos/auto_abstraction_creation/create-topics.sh localhost:9092
```

Start the existing mono binary in one terminal:

```bash
cd /Users/ogbanugot/Workspace/aveni/avenieca
export LIBRARY_PATH=/opt/homebrew/opt/openblas/lib:${LIBRARY_PATH}
./target/release/avenieca mono --config ../eca_demos/auto_abstraction_creation/configs/mono.json
```

Start the server binary in a second terminal:

```bash
cd /Users/ogbanugot/Workspace/aveni/avenieca
export LIBRARY_PATH=/opt/homebrew/opt/openblas/lib:${LIBRARY_PATH}
./target/release/server --config ../eca_demos/auto_abstraction_creation/configs/server.json
```

Stream the data from a third terminal:

```bash
cd /Users/ogbanugot/Workspace/aveni/eca_demos/auto_abstraction_creation
python run_demo.py
```

Run the explicit learning pass through the API:

```bash
cd /Users/ogbanugot/Workspace/aveni/eca_demos/auto_abstraction_creation
python api_stage_learning.py
```

Inspect learned abstractions through the API:

```bash
cd /Users/ogbanugot/Workspace/aveni/eca_demos/auto_abstraction_creation
python api_inspect.py
```

This now follows the same runtime shape as `smart_iot`, with an explicit two-phase flow:

1. stream experience into the source twin
2. stage the learning pass into `core-aa` through the existing server API
3. inspect learned abstractions through that same API

- Postgres on `localhost:5432`
- Qdrant on `http://localhost:6334`
- Kafka on `127.0.0.1:9092`
- Server API on `http://localhost:2580/v1`
- Default API login: `default@email.com` / `admin`
