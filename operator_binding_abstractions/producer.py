import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "avenieca-python"))

from avenieca import Signal
from avenieca.config.broker import Broker
from avenieca.producers import Event

from config import twin_config


def load_rows():
    data_path = Path(__file__).resolve().parent / "data" / "board_states.jsonl"
    rows = []
    for line in data_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        rows.append(json.loads(line))
    return rows


def publish_data():
    broker = twin_config()["broker_config"]
    event = Event(
        config=Broker(
            url=broker["url"],
            digital_twin_topic=broker["subscribe"],
            physical_twin_topic=broker["publish"],
        )
    )
    rows = load_rows()

    for row in rows:
        signal = Signal(
            state=[float(value) for value in row["state"]],
            valence=row.get("valence"),
            score=row.get("score"),
        )
        print(f"publishing {row.get('label', 'state')} -> {signal.state}")
        future = event.publish(signal)
        _ = future.get(timeout=60)
        time.sleep(0.5)


if __name__ == "__main__":
    publish_data()
