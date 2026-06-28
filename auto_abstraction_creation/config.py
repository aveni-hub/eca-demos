import json
import os
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_LICENSE = ROOT / "eca_demos" / "smart_iot" / "license.lic"
SOURCE_ID = "autoabs_src"
PAG_ID = "autoabs_pag"
CORE_PP_ID = "autoabs_pp"
CORE_AA_ID = "autoabs_aa"


def vse_config() -> dict:
    vse_url = os.getenv("VSE_URL", "http://localhost:6334")
    return {
        "client_type": "qdrant",
        "url": vse_url,
        "qdrant_config": {
            "vse_url": vse_url,
            "similarity_metric": "euclid",
            "hnsw_config": {
                "full_scan_threshold": 10000,
                "max_indexing_threads": 0,
                "m": 16,
                "ef_construct": 100,
            },
            "wal_config": {
                "wal_capacity_mb": 32,
                "wal_segments_ahead": 0,
            },
            "optimizer_config": {
                "deleted_threshold": 0.2,
                "vacuum_min_vector_number": 1000,
                "default_segment_number": 0,
                "max_segment_size": None,
                "memmap_threshold": None,
                "indexing_threshold": 2000,
                "flush_interval_sec": 5,
                "max_optimization_threads": 1,
            },
            "shard_number": 1,
            "on_disk_payload": False,
            "timeout": 10,
        },
        "pgvector_config": None,
    }


def license_config() -> dict:
    license_path = os.getenv("LICENSE_PATH")
    if license_path:
        return {"online": None, "offline": {"license_file": license_path}}
    if DEFAULT_LICENSE.exists():
        return {
            "online": None,
            "offline": {"license_file": str(DEFAULT_LICENSE)},
        }
    return {"online": None, "offline": None}


def twin_config() -> dict:
    return {
        "db_config": {
            "table": SOURCE_ID,
            "uri": os.getenv("DB_URL", "postgres://postgres:postgrespw@localhost:5432"),
        },
        "vse_config": vse_config(),
        "log_config": {
            "level": "info",
            "log_file": "/tmp/autoabs_source.log",
            "sentry": None,
        },
        "license_config": license_config(),
        "digital_twin_type": "streamer",
        "physical_twin_type": "sensor",
        "shape": [3, 3],
        "display_name": "Auto Abstraction Source Stream",
        "module_id": SOURCE_ID,
        "duration_threshold": "1s",
        "sync_rate": "250ms",
        "sync_once": False,
        "broker_config": {
            "url": os.getenv("KAFKA_URL", "127.0.0.1:9092"),
            "subscribe": "auto_abstraction_source_sub",
            "publish": "",
        },
        "ras_config": None,
        "in_twins": [],
        "out_twins": [],
    }


def pag_twin_config() -> dict:
    source = twin_config()
    return {
        "db_config": {
            "table": PAG_ID,
            "uri": os.getenv("DB_URL", "postgres://postgres:postgrespw@localhost:5432"),
        },
        "vse_config": vse_config(),
        "log_config": {
            "level": "info",
            "log_file": "/tmp/autoabs_pag.log",
            "sentry": None,
        },
        "license_config": license_config(),
        "digital_twin_type": "reader",
        "physical_twin_type": "sensor",
        "shape": [3, 3],
        "display_name": "Auto Abstraction PAG",
        "module_id": PAG_ID,
        "duration_threshold": "1s",
        "sync_rate": "250ms",
        "sync_once": False,
        "broker_config": {
            "url": os.getenv("KAFKA_URL", "127.0.0.1:9092"),
            "subscribe": PAG_ID,
            "publish": "",
        },
        "ras_config": None,
        "in_twins": [source],
        "out_twins": [],
    }


def core_config(module_id: str, db_table: str, log_file: str) -> dict:
    source = twin_config()
    pag = pag_twin_config()
    return {
        "module_id": module_id,
        "pag": pag["module_id"],
        "recall": 16,
        "valence_threshold": -10.0,
        "range": 16,
        "sync_rate": "250ms",
        "duration_threshold": "1s",
        "sync_once": False,
        "twin_configs": [source, pag],
        "db_config": {
            "table": db_table,
            "uri": os.getenv("DB_URL", "postgres://postgres:postgrespw@localhost:5432"),
        },
        "embedding_config": None,
        "document_config": None,
        "log_config": {
            "level": "info",
            "log_file": log_file,
            "sentry": None,
        },
        "license_config": license_config(),
    }


def mono_config() -> dict:
    source = twin_config()
    pag = pag_twin_config()
    return {
        "twins": [source, pag],
        "corepp_config": core_config(
            CORE_PP_ID,
            CORE_PP_ID,
            "/tmp/autoabs_core_pp.log",
        ),
        "coreaa_config": core_config(
            CORE_AA_ID,
            CORE_AA_ID,
            "/tmp/autoabs_core_aa.log",
        ),
        "coreres_config": None,
        "coreus_config": None,
        "document_config": None,
        "log_config": {
            "level": "info",
            "log_file": "/tmp/auto_abstraction_mono.log",
            "sentry": None,
        },
        "license_config": license_config(),
    }


def server_config() -> dict:
    return {
        "host": "0.0.0.0",
        "port": "2580",
        "cors_max_age": 3600,
        "user_config": {
            "username": os.getenv("USERNAME", "default@email.com"),
            "password": os.getenv("PASSWORD", "admin"),
            "db_config": {
                "table": "user_avenieca",
                "uri": os.getenv("DB_URL", "postgres://postgres:postgrespw@localhost:5432"),
            },
        },
        "cortex_config": core_config(
            CORE_AA_ID,
            CORE_AA_ID,
            "/tmp/autoabs_core_aa.log",
        ),
        "log_config": {
            "level": "info",
            "log_file": "/tmp/auto_abstraction_server.log",
            "sentry": None,
        },
        "license_config": license_config(),
    }


def write_json(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    out = Path(__file__).resolve().parent / "configs"
    write_json(out / "source_twin.json", {"twin": twin_config()})
    write_json(
        out / "core_pp.json",
        {
            "cortex": core_config(
                CORE_PP_ID,
                CORE_PP_ID,
                "/tmp/autoabs_core_pp.log",
            )
        },
    )
    write_json(
        out / "core_aa.json",
        {
            "cortex": core_config(
                CORE_AA_ID,
                CORE_AA_ID,
                "/tmp/autoabs_core_aa.log",
            )
        },
    )
    write_json(out / "mono.json", {"mono": mono_config()})
    write_json(out / "server.json", {"server": server_config()})
