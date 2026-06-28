import os

from avenieca.config.broker import Broker
from avenieca.config.cortex import Cortex, CortexConfig
from avenieca.config.db import DB
from avenieca.config.document import Document, DocumentConfig
from avenieca.config.embedding import Embedding
from avenieca.config.license import License, Offline
from avenieca.config.log import Log
from avenieca.config.retrieval import Retrieval, OAIConfig
from avenieca.config.server import WebAPI, User, ServerConfig
from dotenv import load_dotenv
from avenieca.config.twin import Twin, TwinConfig
from avenieca.config.vse import VSE, HNSW, Optimizer, WAL

load_dotenv()

db_url = os.getenv("DB_DOCKER_URL")
kafka_url = os.getenv("KAFKA_DOCKER_URL")
vse_env = os.getenv("VSE_DOCKER_URL")
openai_url = os.getenv("OPENAI_URL")
openai_key = os.getenv("OPENAI_API_KEY")
username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")
api_key = os.getenv("API_KEY")
license_file = os.getenv("LICENSE_PATH_DOCKER")

btc_twin_config = Twin(
    display_name="BTC",
    module_id="btc",
    physical_twin_type="actuator",
    shape=1,
    broker_config=Broker(
        url=kafka_url,
        sub_topic="btc_sub",
        pub_topic="btc_pub",
        group="actuators",
        auto_offset_reset="latest"
    ),
    db_config=DB(
        uri=db_url,
        table="btc"
    ),
    vse_config=VSE(
        vse_url=vse_env,
        hnsw_config=HNSW(),
        optimizer_config=Optimizer(),
        shard_number=None,
        wal_config=WAL()
    ),
    log_config=Log(
        level="error",
        log_file="/tmp/btc.log"
    ),
    license_config=License(
        offline=Offline(
            license_file=license_file
        )
    )
)

core_pp = Cortex(
    pag=btc_twin_config.module_id,
    name="core",
    recall=20,
    range=20,
    sync_once=False,
    sync_rate="500ms",
    duration_threshold="1s",
    twin_configs=[
        btc_twin_config,
    ],
    db_config=DB(
        table="core",
        uri=db_url
    ),
    log_config=Log(
        level="error",
        log_file="/tmp/cryp_avenieca_corepp.log"
    ),
    license_config=License(
        offline=Offline(
            license_file=license_file
        )
    )
)

core_respond = Cortex(
    pag=btc_twin_config.module_id,
    name="core",
    recall=20,
    range=20,
    sync_once=False,
    sync_rate="200ms",
    duration_threshold="2s",
    twin_configs=[
        btc_twin_config,
    ],
    db_config=DB(
        table="core",
        uri=db_url
    ),
    log_config=Log(
        level="error",
        log_file="/tmp/cryp_avenieca_core_respond.log"
    ),
    license_config=License(
        offline=Offline(
            license_file=license_file
        )
    )
)

core_us = Cortex(
    pag=btc_twin_config.module_id,
    name="core",
    recall=20,
    range=20,
    sync_once=False,
    sync_rate="100ms",
    duration_threshold="2s",
    twin_configs=[
        btc_twin_config,
    ],
    db_config=DB(
        table="core",
        uri=db_url
    ),
    log_config=Log(
        level="error",
        log_file="/tmp/avenieca_core_us.log"
    ),
    license_config=License(
        offline=Offline(
            license_file=license_file
        )
    )
)

document_config = Document(
    name="crypto_docs",
    sync_rate="50ms",
    create_n_embed=True,
    twin_config=btc_twin_config,
    db_config=DB(
        table="crypto_docs",
        uri=db_url
    ),
    vse_config=VSE(
        vse_url=vse_env,
        hnsw_config=HNSW(),
        optimizer_config=Optimizer(),
        shard_number=None,
        wal_config=WAL()
    ),
    log_config=Log(
        level="error",
        log_file="/tmp/cryp_docs.log"
    ),
    embedding_config=Embedding(
        api="openai",
        api_url=openai_url,
        api_key=openai_key,
        model="text-embedding-ada-002",
        embedding_size=1536
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
            table="user_avenieca",
            uri=db_url
        ),
    ),
    log_config=Log(
        level="debug",
        log_file="/tmp/eca_server.log"
    ),
    document_config=document_config,
    retrieval_config=Retrieval(
        api="openai",
        oai_config=OAIConfig(
            api_key=openai_key,
            api_url=openai_url,
            model="gpt-3.5-turbo"
        ),
        document_config=document_config
    ),
    license_config=License(
        offline=Offline(
            license_file=license_file
        )
    )
)

if __name__ == '__main__':
    btc_twin_config = TwinConfig(
        twin=btc_twin_config
    )
    btc_twin_config.to_json_file("configs/docker/twins/btc.json")

    core_pp_config = CortexConfig(
        cortex=core_pp
    )
    core_pp_config.to_json_file("configs/docker/core_pp.json")
    core_us_config = CortexConfig(
        cortex=core_us
    )
    core_us_config.to_json_file("configs/docker/core_us.json")
    core_respond_config = CortexConfig(
        cortex=core_respond
    )
    core_respond_config.to_json_file("configs/docker/core_res.json")
    document_config = DocumentConfig(
        document=document_config
    )
    document_config.to_json_file("configs/docker/document.json")
    server_config = ServerConfig(
        server=server_config
    )
    server_config.to_json_file("configs/docker/server.json")
