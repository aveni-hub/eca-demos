from pathlib import Path
import os
import subprocess
import sys

DEMO_ROOT = Path(__file__).resolve().parent


def main() -> int:
    env = os.environ.copy()
    env.setdefault("KAFKA_URL", "127.0.0.1:9092")
    cmd = [sys.executable, "producer.py"]
    return subprocess.run(cmd, cwd=DEMO_ROOT, env=env, check=False).returncode


if __name__ == "__main__":
    sys.exit(main())
