import os

from avenieca.config.broker import Broker
from avenieca.config.cortex import Cortex, CortexConfig
from avenieca.config.db import DB
from avenieca.config.document import Document, DocumentConfig
from avenieca.config.embedding import Embedding
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
path_docker_volume = os.getenv("FILE_PATH_DOCKER_VOLUME")
path_twins = os.getenv("FILE_PATH_TWINS_DOCKER")
path_ras = os.getenv("FILE_PATH_RAS_DOCKER")
path = os.getenv("FILE_PATH_DOCKER")

event_file = "event"
event_twin_config = Twin(
    display_name="Event",
    module_id="recsys_event",
    physical_twin_type="sensor",
    shape=1536,
    broker_config=Broker(
        url=kafka_url,
        sub_topic="event_sub",
        pub_topic="",
        group="recsys_sensors",
        auto_offset_reset="latest"
    ),
    db_config=DB(
        uri=db_url,
        table="recsys_event"
    ),
    vse_config=VSE(
        vse_url=vse_env,
        hnsw_config=HNSW(),
        optimizer_config=Optimizer(),
        shard_number=None,
        wal_config=WAL()
    ),
    log_config=Log(
        level="info",
        log_file="/tmp/%s.log" % event_file
    ),
)

item_file = "item"
item_twin_config = Twin(
    display_name="Item",
    module_id="recsys_item",
    physical_twin_type="sensor",
    shape=1536,
    broker_config=Broker(
        url=kafka_url,
        sub_topic="item_sub",
        pub_topic="",
        group="recsys_sensors",
        auto_offset_reset="latest"
    ),
    db_config=DB(
        uri=db_url,
        table="recsys_item"
    ),
    vse_config=VSE(
        vse_url=vse_env,
        hnsw_config=HNSW(),
        optimizer_config=Optimizer(),
        shard_number=None,
        wal_config=WAL()
    ),
    log_config=Log(
        level="info",
        log_file="/tmp/%s.log" % item_file
    )
)

aggregate_file = "gwp_aggregate"
aggregate_config = Twin(
    display_name="Recsys_Aggregate",
    module_id="recsys_aggregate",
    shape=3072,
    sync_rate="1s",
    physical_twin_type="sensor",
    duration_threshold="5s",
    in_twins=[
        event_twin_config,
        item_twin_config,
    ],
    db_config=DB(
        table="recsys_aggregate",
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
        level="info",
        log_file="/tmp/%s.log" % aggregate_file
    )
)
twin_configs = [
    event_twin_config,
    item_twin_config,
    aggregate_config,
]

core_pp_file = "recsys_corepp"
core_name = "recsys_core"
core_pp = Cortex(
    name=core_name,
    pag=aggregate_config.module_id,
    recall=20,
    range=20,
    sync_once=False,
    sync_rate="500ms",
    duration_threshold="1s",
    twin_configs=twin_configs,
    db_config=DB(
        table=core_name,
        uri=db_url
    ),
    log_config=Log(
        level="info",
        log_file="/tmp/%s.log" % core_pp_file
    )
)
core_res_file = "recsys_core_res"
core_respond = Cortex(
    name=core_name,
    pag=aggregate_config.module_id,
    recall=20,
    range=20,
    sync_once=False,
    sync_rate="200ms",
    duration_threshold="2s",
    twin_configs=twin_configs,
    db_config=DB(
        table=core_name,
        uri=db_url
    ),
    log_config=Log(
        level="info",
        log_file="/tmp/%s.log" % core_res_file
    )
)
core_us_file = "recsys_core_us"
core_us = Cortex(
    name=core_name,
    pag=aggregate_config.module_id,
    recall=20,
    range=20,
    sync_once=False,
    sync_rate="100ms",
    duration_threshold="2s",
    twin_configs=twin_configs,
    db_config=DB(
        table="recsys_core",
        uri=db_url
    ),
    log_config=Log(
        level="info",
        log_file="/tmp/%s.log" % core_us_file
    )
)
document_file = "recsys_docs"
document_config = Document(
    name="recsys_docs",
    sync_rate="50ms",
    create_n_embed=True,
    twin_config=aggregate_config,
    db_config=DB(
        table="recsys_docs",
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
        level="info",
        log_file="/tmp/%s.log" % document_file
    ),
    embedding_config=Embedding(
        api="openai",
        api_url=openai_url,
        api_key=openai_key,
        model="text-embedding-ada-002",
        embedding_size=1536
    )
)
server_file = "recsys_server"
server_config = WebAPI(
    cortex_config=core_pp,
    user_config=User(
        username=username,
        password=password,
        api_key=api_key,
        db_config=DB(
            table="recsys_users",
            uri=db_url
        ),
    ),
    log_config=Log(
        level="debug",
        log_file="/tmp/%s.log" % server_file
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
    )
)

if __name__ == '__main__':
    '''Event'''
    event_twin_config = TwinConfig(
        twin=event_twin_config
    )
    event_twin_config.to_json_file(
        "%s/%s.json" % (path_twins, event_file))

    '''Item'''
    item_twin_config = TwinConfig(
        twin=item_twin_config
    )
    item_twin_config.to_json_file(
        "%s/%s.json" % (path_twins, item_file))

    '''Aggregate'''
    aggregate_config = TwinConfig(
        twin=aggregate_config
    )
    aggregate_config.to_json_file("%s/%s.json" % (path_twins, aggregate_file))

    '''Core-PP'''
    core_pp_config = CortexConfig(
        cortex=core_pp
    )
    core_pp_config.to_json_file("%s/%s.json" % (path, core_pp_file))

    '''Core-US'''
    core_us_config = CortexConfig(
        cortex=core_us
    )
    core_us_config.to_json_file("%s/%s.json" % (path, core_us_file))

    '''Core-Respond'''
    core_respond_config = CortexConfig(
        cortex=core_respond
    )
    core_respond_config.to_json_file("%s/%s.json" % (path, core_res_file))

    '''Document'''
    document_config = DocumentConfig(
        document=document_config
    )
    document_config.to_json_file("%s/%s.json" % (path, document_file))

    '''Server'''
    server_config = ServerConfig(
        server=server_config
    )
    server_config.to_json_file("%s/%s.json" % (path, server_file))

    yaml_twins = {
        'version': '3',
        'services':
            {
                'ac': {
                    'image': 'ogbanugot/avenieca:0.3.0',
                    'command': 'twin --config "/avenieca/ac.json"',
                    'volumes': ['ac:/avenieca/storage', './configs/docker/twins/ac.json:/avenieca/ac.json',
                                './configs/docker/ras/ac_ras.json:/avenieca/ac_ras.json'], 'networks': ['ECACluster'],
                    'deploy': {'restart_policy': {'condition': 'on-failure', 'delay': '2s', 'max_attempts': 20,
                                                  'window': '120s'}}},
                'aqi': {'image': 'ogbanugot/avenieca:0.3.0', 'command': 'twin --config "/avenieca/aqi.json"',
                        'volumes': ['aqi:/avenieca/storage', './configs/docker/twins/aqi.json:/avenieca/aqi.json',
                                    './configs/docker/ras/aqi_ras.json:/avenieca/aqi_ras.json'],
                        'networks': ['ECACluster'],
                        'deploy': {'restart_policy': {'condition': 'on-failure', 'delay': '2s', 'max_attempts': 20,
                                                      'window': '120s'}}},
                'occupancy': {'image': 'ogbanugot/avenieca:0.3.0',
                              'command': 'twin --config "/avenieca/occupancy.json"',
                              'volumes': ['occupancy:/avenieca/storage',
                                          './configs/docker/twins/occupancy.json:/avenieca/occupancy.json',
                                          './configs/docker/ras/occupancy_ras.json:/avenieca/occupancy_ras.json'],
                              'networks': ['ECACluster'],
                              'deploy': {
                                  'restart_policy': {'condition': 'on-failure', 'delay': '2s', 'max_attempts': 20,
                                                     'window': '120s'}}},
                'purifier': {'image': 'ogbanugot/avenieca:0.3.0', 'command': 'twin --config "/avenieca/purifier.json"',
                             'volumes': ['purifier:/avenieca/storage',
                                         './configs/docker/twins/purifier.json:/avenieca/purifier.json',
                                         './configs/docker/ras/purifier_ras.json:/avenieca/purifier_ras.json'],
                             'networks': ['ECACluster'],
                             'deploy': {
                                 'restart_policy': {'condition': 'on-failure', 'delay': '2s', 'max_attempts': 20,
                                                    'window': '120s'}}},
                'temperature': {'image': 'ogbanugot/avenieca:0.3.0',
                                'command': 'twin --config "/avenieca/temperature.json"',
                                'volumes': [
                                    'temperature:/avenieca/storage',
                                    './configs/docker/twins/temperature.json:/avenieca/temperature.json',
                                    './configs/docker/ras/temperature_ras.json:/avenieca/temperature_ras.json'],
                                'networks': ['ECACluster'],
                                'deploy': {
                                    'restart_policy': {'condition': 'on-failure', 'delay': '2s', 'max_attempts': 20,
                                                       'window': '120s'}}}
            },
        'volumes': {'ac': {'driver': 'local'}, 'aqi': {'driver': 'local'}, 'occupancy': {'driver': 'local'},
                    'temperature': {'driver': 'local'}, 'purifier': {'driver': 'local'}},
        'networks': {'ECACluster': None}}
