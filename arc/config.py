import os

from avenieca.config.broker import Broker
from avenieca.config.cortex import Cortex, CortexConfig
from avenieca.config.db import DB
from avenieca.config.license import License, Offline
from avenieca.config.log import Log
from avenieca.config.server import WebAPI, User, ServerConfig
from dotenv import load_dotenv
from avenieca.config.twin import Twin, TwinConfig
from avenieca.config.vse import VSE, HNSW, Optimizer, WAL

load_dotenv()

db_url = os.getenv("DB_URL")
kafka_url = os.getenv("KAFKA_URL")
vse_env = os.getenv("VSE_URL")
openai_url = os.getenv("OPENAI_URL")
openai_key = os.getenv("OPENAI_API_KEY")
username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")
api_key = os.getenv("API_KEY")
license_file = os.getenv("LICENSE_PATH")
path_ras = os.getenv("FILE_PATH_RAS")
path = os.getenv("FILE_PATH")

cell_config = Twin(
    display_name="ARC Cell",
    module_id="arc_cell",
    physical_twin_type="actuator",
    shape=1,
    broker_config=Broker(
        url=kafka_url,
        sub_topic="arc_cell_sub",
        pub_topic="arc_cell_pub",
        group="arc_cell_actuators",
        auto_offset_reset="latest"
    ),
    db_config=DB(
        uri=db_url,
        table="arc_cell"
    ),
    vse_config=VSE(
        hnsw_config=HNSW(),
        optimizer_config=Optimizer(),
        shard_number=None,
        wal_config=WAL()
    ),
    log_config=Log(
        level="info",
        log_file="/tmp/arc_cell.log"
    ),
    license_config=License(
        offline=Offline(
            license_file=license_file
        )
    )
)

core_pp = Cortex(
    pag=cell_config.module_id,
    name="core",
    recall=297,
    range=297,
    sync_once=False,
    sync_rate="100ms",
    duration_threshold="1s",
    twin_configs=[
        cell_config,
    ],
    db_config=DB(
        table="core",
        uri=db_url
    ),
    log_config=Log(
        level="info",
        log_file="/tmp/arc_corepp.log"
    ),
    license_config=License(
        offline=Offline(
            license_file=license_file
        )
    )
)

core_respond = Cortex(
    pag=cell_config.module_id,
    name="core",
    recall=20,
    range=20,
    sync_once=False,
    sync_rate="50ms",
    duration_threshold="1s",
    twin_configs=[
        cell_config,
    ],
    db_config=DB(
        table="core",
        uri=db_url
    ),
    log_config=Log(
        level="info",
        log_file="/tmp/arc_core_respond.log"
    ),
    license_config=License(
        offline=Offline(
            license_file=license_file
        )
    )
)

core_us = Cortex(
    pag=cell_config.module_id,
    name="core",
    recall=20,
    range=20,
    sync_once=False,
    sync_rate="20ms",
    duration_threshold="1s",
    twin_configs=[
        cell_config,
    ],
    db_config=DB(
        table="core",
        uri=db_url
    ),
    log_config=Log(
        level="info",
        log_file="/tmp/arc_core_us.log"
    ),
    license_config=License(
        offline=Offline(
            license_file=license_file
        )
    )
)

server_config = WebAPI(
    cortex_config=core_pp,
    user_config=User(
        username=username,
        password=password,
        api_key=api_key,
        db_config=DB(
            table="user_arc_avenieca",
            uri=db_url
        ),
    ),
    log_config=Log(
        level="info",
        log_file="/tmp/arc_server.log"
    ),
    license_config=License(
        offline=Offline(
            license_file=license_file
        )
    )
)

if __name__ == '__main__':
    cell_twin_config = TwinConfig(
        twin=cell_config
    )
    cell_twin_config.to_json_file("configs/twins/arc_cell.json")
    core_pp_config = CortexConfig(
        cortex=core_pp
    )
    core_pp_config.to_json_file("configs/core_pp.json")

    core_us_config = CortexConfig(
        cortex=core_us
    )
    core_us_config.to_json_file("configs/core_us.json")

    core_respond_config = CortexConfig(
        cortex=core_respond
    )
    core_respond_config.to_json_file("configs/core_res.json")

    server_config = ServerConfig(
        server=server_config
    )
    server_config.to_json_file("configs/server.json")
