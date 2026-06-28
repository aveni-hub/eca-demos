import os

from avenieca.config.broker import Broker
from avenieca.config.cortex import Cortex, CortexConfig
from avenieca.config.db import DB
from avenieca.config.document import Document, DocumentConfig, Retrieval, LlmProvider
from avenieca.config.embedding import Embedding
from avenieca.config.license import License, Offline
from avenieca.config.log import Log, Sentry
from avenieca.config.ras import RAS, EmotifiedInstances, ESI, EmotifiedInstancesConfig
from avenieca.config.server import WebAPI, User, ServerConfig
from dotenv import load_dotenv
from avenieca.config.twin import Twin, TwinConfig
from avenieca.config.vse import VSE, HNSW, Optimizer, WAL
from avenieca.config.mono import Mono, MonoConfig

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
sentry_dsn = os.getenv("SENTRY_DSN")

ac_twin_config = Twin(
    display_name="Air Conditioner",
    module_id="air_conditioner",
    digital_twin_type="streamer",
    physical_twin_type="actuator",
    shape=1,
    broker_config=Broker(
        url=kafka_url,
        digital_twin_topic="ac_sub",
        physical_twin_topic="ac_pub",
    ),
    db_config=DB(
        uri=db_url,
        table="ac"
    ),
    vse_config=VSE(
        hnsw_config=HNSW(),
        optimizer_config=Optimizer(),
        shard_number=None,
        wal_config=WAL()
    ),
    log_config=Log(
        level="info",
        log_file="/tmp/ac.log"
    ),
    ras_config=RAS(
        upsert_from="json",
        file_path="%s/ac_ras.json" % path_ras
    ),
    license_config=License(
        offline=Offline(
            license_file=license_file
        )
    )
)


gi_twin_config = Twin(
    display_name="General Instructions",
    module_id="instructions",
    digital_twin_type="streamer",
    physical_twin_type="actuator",
    shape=1,
    broker_config=Broker(
        url=kafka_url,
        digital_twin_topic="gi_sub",
        physical_twin_topic="gi_pub",
    ),
    db_config=DB(
        uri=db_url,
        table="gi"
    ),
    vse_config=VSE(
        hnsw_config=HNSW(),
        optimizer_config=Optimizer(),
        shard_number=None,
        wal_config=WAL()
    ),
    log_config=Log(
        level="info",
        log_file="/tmp/gi.log"
    ),
    license_config=License(
        offline=Offline(
            license_file=license_file
        )
    )
)

sp_twin_config = Twin(
    display_name="Speedometer",
    module_id="speedometer",
    digital_twin_type="streamer",
    physical_twin_type="actuator",
    shape=1,
    broker_config=Broker(
        url=kafka_url,
        digital_twin_topic="ac_sub",
        physical_twin_topic="ac_pub",
    ),
    db_config=DB(
        uri=db_url,
        table="speedometer"
    ),
    vse_config=VSE(
        hnsw_config=HNSW(),
        optimizer_config=Optimizer(),
        shard_number=None,
        wal_config=WAL()
    ),
    log_config=Log(
        level="info",
        log_file="/tmp/ac.log"
    ),
    ras_config=RAS(
        upsert_from="json",
        file_path="%s/ac_ras.json" % path_ras
    ),
    license_config=License(
        offline=Offline(
            license_file=license_file
        )
    )
)

od_twin_config = Twin(
    display_name="Odometer",
    module_id="odometer",
    digital_twin_type="streamer",
    physical_twin_type="actuator",
    shape=1,
    broker_config=Broker(
        url=kafka_url,
        digital_twin_topic="ac_sub",
        physical_twin_topic="ac_pub",
    ),
    db_config=DB(
        uri=db_url,
        table="odometer"
    ),
    vse_config=VSE(
        hnsw_config=HNSW(),
        optimizer_config=Optimizer(),
        shard_number=None,
        wal_config=WAL()
    ),
    log_config=Log(
        level="info",
        log_file="/tmp/ac.log"
    ),
    ras_config=RAS(
        upsert_from="json",
        file_path="%s/ac_ras.json" % path_ras
    ),
    license_config=License(
        offline=Offline(
            license_file=license_file
        )
    )
)

cam_twin_config = Twin(
    display_name="Camera",
    module_id="camera001",
    digital_twin_type="streamer",
    physical_twin_type="actuator",
    shape=1,
    broker_config=Broker(
        url=kafka_url,
        digital_twin_topic="ac_sub",
        physical_twin_topic="ac_pub",
    ),
    db_config=DB(
        uri=db_url,
        table="camera001"
    ),
    vse_config=VSE(
        hnsw_config=HNSW(),
        optimizer_config=Optimizer(),
        shard_number=None,
        wal_config=WAL()
    ),
    log_config=Log(
        level="info",
        log_file="/tmp/ac.log"
    ),
    ras_config=RAS(
        upsert_from="json",
        file_path="%s/ac_ras.json" % path_ras
    ),
    license_config=License(
        offline=Offline(
            license_file=license_file
        )
    )
)

rotor_twin_config = Twin(
    display_name="Rotor",
    module_id="rotor",
    digital_twin_type="streamer",
    physical_twin_type="actuator",
    shape=1,
    broker_config=Broker(
        url=kafka_url,
        digital_twin_topic="ac_sub",
        physical_twin_topic="ac_pub",
    ),
    db_config=DB(
        uri=db_url,
        table="rotor"
    ),
    vse_config=VSE(
        hnsw_config=HNSW(),
        optimizer_config=Optimizer(),
        shard_number=None,
        wal_config=WAL()
    ),
    log_config=Log(
        level="info",
        log_file="/tmp/ac.log"
    ),
    ras_config=RAS(
        upsert_from="json",
        file_path="%s/ac_ras.json" % path_ras
    ),
    license_config=License(
        offline=Offline(
            license_file=license_file
        )
    )
)

ac_twin_ras = EmotifiedInstances(
    esi_vec=[
        ESI(
            id=1,
            state_vec=[22],
            valence=90.0
        )
    ]
)

aqi_twin_config = Twin(
    display_name="Air Quality Index",
    module_id="air_quality_index",
    digital_twin_type="streamer",
    physical_twin_type="sensor",
    shape=1,
    broker_config=Broker(
        url=kafka_url,
        digital_twin_topic="aqi_sub",
        physical_twin_topic="",
    ),
    db_config=DB(
        uri=db_url,
        table="aqi"
    ),
    vse_config=VSE(
        hnsw_config=HNSW(),
        optimizer_config=Optimizer(),
        shard_number=None,
        wal_config=WAL()
    ),
    log_config=Log(
        level="info",
        log_file="/tmp/aqi.log"
    ),
    ras_config=RAS(
        upsert_from="json",
        file_path="%s/aqi_ras.json" % path_ras
    ),
    license_config=License(
        offline=Offline(
            license_file=license_file
        )
    )
)
aqi_twin_ras = EmotifiedInstances(
    esi_vec=[
        ESI(
            id=1,
            state_vec=[30],
            valence=90.0
        ),
        ESI(
            id=2,
            state_vec=[60],
            valence=-90.0
        )
    ]
)
purifier_twin_config = Twin(
    display_name="Purifier",
    module_id="purifier",
    digital_twin_type="streamer",
    physical_twin_type="actuator",
    shape=1,
    broker_config=Broker(
        url=kafka_url,
        digital_twin_topic="purifier_sub",
        physical_twin_topic="purifier_pub",
    ),
    db_config=DB(
        uri=db_url,
        table="purifier"
    ),
    vse_config=VSE(
        hnsw_config=HNSW(),
        optimizer_config=Optimizer(),
        shard_number=None,
        wal_config=WAL()
    ),
    log_config=Log(
        level="info",
        log_file="/tmp/purifier.log"
    ),
    ras_config=RAS(
        upsert_from="json",
        file_path="%s/purifier_ras.json" % path_ras
    ),
    license_config=License(
        offline=Offline(
            license_file=license_file
        )
    )
)
purifier_twin_ras = EmotifiedInstances(
    esi_vec=[
        ESI(
            id=1,
            state_vec=[1],
            valence=90.0
        ),
        ESI(
            id=2,
            state_vec=[0],
            valence=-90.0
        )
    ]
)
occupancy_twin_config = Twin(
    display_name="Occupancy",
    module_id="occupancy",
    digital_twin_type="streamer",
    physical_twin_type="sensor",
    shape=1,
    broker_config=Broker(
        url=kafka_url,
        digital_twin_topic="occupancy_sub",
        physical_twin_topic="",
    ),
    db_config=DB(
        uri=db_url,
        table="occupancy"
    ),
    vse_config=VSE(
        hnsw_config=HNSW(),
        optimizer_config=Optimizer(),
        shard_number=None,
        wal_config=WAL()
    ),
    log_config=Log(
        level="info",
        log_file="/tmp/occupancy.log"
    ),
    ras_config=RAS(
        upsert_from="json",
        file_path="%s/occupancy_ras.json" % path_ras
    ),
    license_config=License(
        offline=Offline(
            license_file=license_file
        )
    )
)
occupancy_twin_ras = EmotifiedInstances(
    esi_vec=[
        ESI(
            id=1,
            state_vec=[5],
            valence=90.0
        ),
        ESI(
            id=2,
            state_vec=[10],
            valence=-90.0
        )
    ]
)
temperature_twin_config = Twin(
    display_name="Temperature (Celsius)",
    module_id="temperature",
    digital_twin_type="streamer",
    physical_twin_type="sensor",
    shape=1,
    broker_config=Broker(
        url=kafka_url,
        digital_twin_topic="temperature_sub",
        physical_twin_topic="",
    ),
    db_config=DB(
        uri=db_url,
        table="temperature"
    ),
    vse_config=VSE(
        hnsw_config=HNSW(),
        optimizer_config=Optimizer(),
        shard_number=None,
        wal_config=WAL()
    ),
    log_config=Log(
        level="info",
        log_file="/tmp/temperature.log"
    ),
    ras_config=RAS(
        upsert_from="json",
        file_path="%s/temperature_ras.json" % path_ras
    ),
    license_config=License(
        offline=Offline(
            license_file=license_file
        )
    )
)

temperature_twin_ras = EmotifiedInstances(
    esi_vec=[
        ESI(
            id=1,
            state_vec=[18],
            valence=90.0
        ),
        ESI(
            id=2,
            state_vec=[25],
            valence=-90.0
        )
    ]
)

aggregate_config = Twin(
    display_name="PAG",
    shape=4,
    digital_twin_type="reader",
    physical_twin_type="",
    module_id="aggregate001",
    sync_rate="1s",
    duration_threshold="40s",
    in_twins=[
        ac_twin_config,
        aqi_twin_config,
        purifier_twin_config,
        temperature_twin_config,
    ],
    broker_config=Broker(
        url=kafka_url,
        digital_twin_topic="aggregate001",
        physical_twin_topic="",
    ),
    db_config=DB(
        table="pag",
        uri=db_url
    ),
    vse_config=VSE(
        hnsw_config=HNSW(),
        optimizer_config=Optimizer(),
        shard_number=None,
        wal_config=WAL()
    ),
    log_config=Log(
        level="info",
        log_file="/tmp/aggregate001.log",
    ),
    license_config=License(
        offline=Offline(
            license_file=license_file
        )
    )
)

document_config = Document(
    display_name="smart_building_docs",
    module_id="",
    create_n_embed=True,
    db_config=DB(
        table="smart_building_docs",
        uri=db_url
    ),
    vse_config=VSE(
        hnsw_config=HNSW(),
        optimizer_config=Optimizer(),
        shard_number=None,
        wal_config=WAL()
    ),
    retrieval_config=Retrieval(
        llm_provider_config=LlmProvider(
            provider="openai",
            api_key=openai_key,
            api_url=openai_url,
            model="gpt-3.5-turbo",
        ),
    ),
    embedding_config=Embedding(
        api="openai",
        api_url=openai_url,
        api_key=openai_key,
        model="text-embedding-ada-002",
        embedding_size=1536
    ),
)

core_pp = Cortex(
    pag=aggregate_config.module_id,
    name="core",
    recall=10,
    range=10,
    sync_once=False,
    sync_rate="500ms",
    duration_threshold="1s",
    twin_configs=[
        ac_twin_config,
        aqi_twin_config,
        purifier_twin_config,
        temperature_twin_config,
        aggregate_config,
    ],
    db_config=DB(
        table="core",
        uri=db_url
    ),
    log_config=Log(
        level="info",
        log_file="/tmp/avenieca_corepp.log"
    ),
    document_config=document_config,
    license_config=License(
        offline=Offline(
            license_file=license_file
        )
    )
)

core_respond = Cortex(
    pag=aggregate_config.module_id,
    name="core",
    recall=20,
    range=20,
    sync_once=False,
    sync_rate="200ms",
    duration_threshold="2s",
    twin_configs=[
        ac_twin_config,
        aqi_twin_config,
        purifier_twin_config,
        temperature_twin_config,
        aggregate_config,
    ],
    db_config=DB(
        table="core",
        uri=db_url
    ),
    log_config=Log(
        level="info",
        log_file="/tmp/avenieca_core_respond.log"
    ),
    license_config=License(
        offline=Offline(
            license_file=license_file
        )
    )
)

core_us = Cortex(
    pag=aggregate_config.module_id,
    name="core",
    recall=20,
    range=20,
    sync_once=False,
    sync_rate="100ms",
    duration_threshold="2s",
    twin_configs=[
        ac_twin_config,
        aqi_twin_config,
        purifier_twin_config,
        temperature_twin_config,
        aggregate_config,
    ],
    db_config=DB(
        table="core",
        uri=db_url
    ),
    log_config=Log(
        level="info",
        log_file="/tmp/avenieca_core_us.log"
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
        level="info",
        log_file="/tmp/eca_server.log"
    ),
    license_config=License(
        offline=Offline(
            license_file=license_file
        )
    )
)

node_config = Mono(
    twins=[
        ac_twin_config,
        aqi_twin_config,
        occupancy_twin_config,
        purifier_twin_config,
        temperature_twin_config,
        aggregate_config,
    ],
    corepp_config=core_pp,
    coreus_config=core_us,
    coreres_config=core_respond,
    log_config=Log(
        level="info",
        log_file="/tmp/eca_server.log"
    ),
    license_config=License(
        offline=Offline(
            license_file=license_file
        )
    )
)

if __name__ == '__main__':
    ac_twin_config = TwinConfig(
        twin=ac_twin_config
    )
    ac_twin_ras = EmotifiedInstancesConfig(
        emotified_instances=ac_twin_ras
    )
    ac_twin_ras.to_json_file("configs/ras/ac_ras.json")
    ac_twin_config.to_json_file("configs/twins/ac.json")

    # sp_twin_config = TwinConfig(
    #     twin=sp_twin_config
    # )
    # sp_twin_config.to_json_file("configs/twins/sp.json")

    aqi_twin_config = TwinConfig(
        twin=aqi_twin_config
    )
    aqi_twin_ras = EmotifiedInstancesConfig(
        emotified_instances=aqi_twin_ras
    )
    aqi_twin_ras.to_json_file("configs/ras/aqi_ras.json")
    aqi_twin_config.to_json_file("configs/twins/aqi.json")

    occupancy_twin_config = TwinConfig(
        twin=occupancy_twin_config
    )
    occupancy_twin_ras = EmotifiedInstancesConfig(
        emotified_instances=occupancy_twin_ras
    )
    occupancy_twin_ras.to_json_file("configs/ras/occupancy_ras.json")
    occupancy_twin_config.to_json_file("configs/twins/occupancy.json")

    purifier_twin_config = TwinConfig(
        twin=purifier_twin_config
    )
    purifier_twin_ras = EmotifiedInstancesConfig(
        emotified_instances=purifier_twin_ras
    )
    purifier_twin_ras.to_json_file("configs/ras/purifier_ras.json")
    purifier_twin_config.to_json_file("configs/twins/purifier.json")

    temperature_twin_config = TwinConfig(
        twin=temperature_twin_config
    )
    temperature_twin_ras = EmotifiedInstancesConfig(
        emotified_instances=temperature_twin_ras
    )
    temperature_twin_ras.to_json_file(
        "configs/ras/temperature_ras.json"
    )
    temperature_twin_config.to_json_file(
        "configs/twins/temperature.json"
    )

    aggregate_config = TwinConfig(
        twin=aggregate_config
    )
    aggregate_config.to_json_file("configs/aggregate.json")
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
    document_config = DocumentConfig(
        document=document_config
    )
    document_config.to_json_file("configs/document.json")
    server_config = ServerConfig(
        server=server_config
    )
    server_config.to_json_file("configs/server.json")

    node_config = MonoConfig(
        mono=node_config
    )
    node_config.to_json_file("configs/mono.json")
