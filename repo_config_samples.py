import os

from avenieca.config.broker import Broker
from avenieca.config.cortex import Cortex, CortexConfig
from avenieca.config.db import DB
from avenieca.config.document import Document, DocumentConfig
from avenieca.config.embedding import Embedding
from avenieca.config.log import Log
from avenieca.config.ras import RAS, EmotifiedInstances, ESI, EmotifiedInstancesConfig
from avenieca.config.retrieval import Retrieval, OAIConfig
from avenieca.config.server import WebAPI, User, ServerConfig
from avenieca.config.twin import Twin, TwinConfig
from avenieca.config.vse import VSE, HNSW, Optimizer, WAL


db_url = "<postgres-uri>"
kafka_url = "<kafka-uri>"
vse_env = "<qdrant-url>"
openai_url = "<openai-api uri>"
openai_key = "<OPENAI-API-KEY>"
username = "<username>"
password = "<password>"
api_key = "<api-key>"
path_twins = "/Users/ogbanugot/Workspace/avenieca/src/sample_configs"
path_ras = "/Users/ogbanugot/Workspace/avenieca/src/sample_configs"
path = "/Users/ogbanugot/Workspace/avenieca/src/sample_configs"

twin01_file = "twin"
twin01_twin_config = Twin(
    display_name="twin01",
    module_id="twin01_module",
    physical_twin_type="sensor",
    shape=2,
    broker_config=Broker(
        url=kafka_url,
        sub_topic="twin01_sub",
        pub_topic="",
        group="sample_sensors",
        auto_offset_reset="latest"
    ),
    db_config=DB(
        uri=db_url,
        table="twin01_table"
    ),
    vse_config=VSE(
        hnsw_config=HNSW(),
        optimizer_config=Optimizer(),
        shard_number=None,
        wal_config=WAL()
    ),
    ras_config=RAS(
        upsert_from="json",
        file_path="%s/%s_ras.json" % (path_ras, twin01_file)
    ),
    log_config=Log(
        level="info",
        log_file="/tmp/%s.log" % twin01_file
    ),
)
twin01_twin_ras = EmotifiedInstances(
    esi_vec=[
        ESI(
            id=1,
            state_vec=[22.0, 9.0],
            valence=90.0
        )
    ]
)

aggregate_file = "aggregate"
aggregate_config = Twin(
    display_name="Aggregate",
    module_id="aggregate_001",
    shape=3072,
    sync_rate="1s",
    physical_twin_type="sensor",
    duration_threshold="5s",
    in_twins=[
        twin01_twin_config,
    ],
    db_config=DB(
        table="aggregate",
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
    twin01_twin_config,
    aggregate_config,
]

core_pp_file = "cortex"
core_name = "avenieca_corepp"
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

document_file = "document"
document_config = Document(
    name="sample_document",
    sync_rate="50ms",
    create_n_embed=False,
    twin_config=aggregate_config,
    db_config=DB(
        table="sample_docs",
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
        model="<embedding_model>",
        embedding_size=1536
    )
)
server_file = "server"
server_config = WebAPI(
    cortex_config=core_pp,
    user_config=User(
        username=username,
        password=password,
        api_key=api_key,
        db_config=DB(
            table="sample_users",
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
            model="<completions model>"
        ),
        document_config=document_config
    )
)

if __name__ == '__main__':
    twin01_twin_config = TwinConfig(
        twin=twin01_twin_config
    )
    twin01_twin_config.to_json_file(
        "%s/%s.json" % (path_twins, twin01_file))

    twin01_twin_ras = EmotifiedInstancesConfig(
        emotified_instances=twin01_twin_ras
    )
    twin01_twin_ras.to_json_file("%s/%s_ras.json" % (path_ras, twin01_file))

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
