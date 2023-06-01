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

date_file = "date"
date_twin_config = Twin(
    display_name="GWP-Date",
    module_id="gwp_date",
    physical_twin_type="sensor",
    shape=1536,
    broker_config=Broker(
        url=kafka_url,
        sub_topic="gwp_date_sub",
        pub_topic="",
        group="gwp_sensors",
        auto_offset_reset="latest"
    ),
    db_config=DB(
        uri=db_url,
        table="gwp_date"
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
        log_file="/tmp/%s.log" % date_file
    ),
)

quarter_file = "quarter"
quarter_twin_config = Twin(
    display_name="Quarter",
    module_id="quarter",
    physical_twin_type="sensor",
    shape=1536,
    broker_config=Broker(
        url=kafka_url,
        sub_topic="q_sub",
        pub_topic="",
        group="gwp_sensors",
        auto_offset_reset="latest"
    ),
    db_config=DB(
        uri=db_url,
        table="quarter"
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
        log_file="/tmp/%s.log" % quarter_file
    )
)

department_file = "department"
department_twin_config = Twin(
    display_name="Department",
    module_id="department",
    physical_twin_type="sensor",
    shape=1536,
    broker_config=Broker(
        url=kafka_url,
        sub_topic="department_sub",
        pub_topic="",
        group="gwp_sensors",
        auto_offset_reset="latest"
    ),
    db_config=DB(
        uri=db_url,
        table="department"
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
        log_file="/tmp/%s.log" % department_file
    )
)

day_file = "day"
day_twin_config = Twin(
    display_name="Day",
    module_id="day",
    physical_twin_type="sensor",
    shape=1536,
    broker_config=Broker(
        url=kafka_url,
        sub_topic="day_sub",
        pub_topic="",
        group="gwp_sensors",
        auto_offset_reset="latest"
    ),
    db_config=DB(
        uri=db_url,
        table="day"
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
        log_file="/tmp/%s.log" % day_file
    )
)

team_file = "team"
team_twin_config = Twin(
    display_name="Team",
    module_id="team",
    physical_twin_type="sensor",
    shape=1,
    broker_config=Broker(
        url=kafka_url,
        sub_topic="team_sub",
        pub_topic="",
        group="gwp_sensor",
        auto_offset_reset="latest"
    ),
    db_config=DB(
        uri=db_url,
        table="team"
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
        log_file="/tmp/%s.log" % team_file
    ),
    ras_config=RAS(
        upsert_from="json",
        file_path="%s/%s_ras.json" % (path_ras, team_file)
    )
)
team_twin_ras = EmotifiedInstances(
    esi_vec=[
        ESI(
            id=1,
            state_vec=[11],
            valence=90.0
        ),
    ]
)
targ_prod_file = "targ_prod"
targeted_prod_twin_config = Twin(
    display_name="Targeted Productivity",
    module_id="targeted_productivity",
    physical_twin_type="sensor",
    shape=1,
    broker_config=Broker(
        url=kafka_url,
        sub_topic="targ_prod_sub",
        pub_topic="",
        group="gwp_sensor",
        auto_offset_reset="latest"
    ),
    db_config=DB(
        uri=db_url,
        table="targ_prod"
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
        log_file="/tmp/%s.log" % targ_prod_file
    ),
    ras_config=RAS(
        upsert_from="json",
        file_path="%s/%s_ras.json" % (path_ras, targ_prod_file)
    )
)
targeted_productivity_twin_ras = EmotifiedInstances(
    esi_vec=[
        ESI(
            id=1,
            state_vec=[0.8],
            valence=90.0
        ),
        ESI(
            id=2,
            state_vec=[0.3],
            valence=-90.0
        )
    ]
)
smv_file = "smv"
smv_twin_config = Twin(
    display_name="Standard Minute Value (SMV)",
    module_id="smv",
    physical_twin_type="sensor",
    shape=1,
    broker_config=Broker(
        url=kafka_url,
        sub_topic="smv_sub",
        pub_topic="",
        group="gwp_sensor",
        auto_offset_reset="latest"
    ),
    db_config=DB(
        uri=db_url,
        table="smv"
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
        log_file="/tmp/%s.log" % smv_file
    ),
    ras_config=RAS(
        upsert_from="json",
        file_path="%s/%s_ras.json" % (path_ras, smv_file)
    )
)
smv_twin_ras = EmotifiedInstances(
    esi_vec=[
        ESI(
            id=1,
            state_vec=[98],
            valence=90.0
        ),
    ]
)
wip_file = "wip"
wip_twin_config = Twin(
    display_name="Work in Progress (WIP)",
    module_id="wip",
    physical_twin_type="sensor",
    shape=1,
    broker_config=Broker(
        url=kafka_url,
        sub_topic="wip_sub",
        pub_topic="",
        group="gwp_sensor",
        auto_offset_reset="latest"
    ),
    db_config=DB(
        uri=db_url,
        table="wip"
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
        log_file="/tmp/%s.log" % wip_file
    ),
    ras_config=RAS(
        upsert_from="json",
        file_path="%s/%s_ras.json" % (path_ras, wip_file)
    )
)
wip_twin_ras = EmotifiedInstances(
    esi_vec=[
        ESI(
            id=1,
            state_vec=[1260],
            valence=-90.0
        ),
        ESI(
            id=1,
            state_vec=[600],
            valence=90.0
        ),
    ]
)
overtime_file = "overtime"
overtime_twin_config = Twin(
    display_name="Overtime",
    module_id="overtime",
    physical_twin_type="sensor",
    shape=1,
    broker_config=Broker(
        url=kafka_url,
        sub_topic="overtime_sub",
        pub_topic="",
        group="gwp_sensor",
        auto_offset_reset="latest"
    ),
    db_config=DB(
        uri=db_url,
        table="overtime"
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
        log_file="/tmp/%s.log" % overtime_file
    ),
    ras_config=RAS(
        upsert_from="json",
        file_path="%s/%s_ras.json" % (path_ras, overtime_file)
    )
)
overtime_twin_ras = EmotifiedInstances(
    esi_vec=[
        ESI(
            id=1,
            state_vec=[1260],
            valence=-90.0
        ),
        ESI(
            id=1,
            state_vec=[600],
            valence=90.0
        ),
    ]
)
now_file = "now"
now_twin_config = Twin(
    display_name="No of Workers",
    module_id="no_of_workers",
    physical_twin_type="sensor",
    shape=1,
    broker_config=Broker(
        url=kafka_url,
        sub_topic="now_sub",
        pub_topic="",
        group="gwp_sensor",
        auto_offset_reset="latest"
    ),
    db_config=DB(
        uri=db_url,
        table="now"
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
        log_file="/tmp/%s.log" % now_file
    ),
    ras_config=RAS(
        upsert_from="json",
        file_path="%s/%s_ras.json" % (path_ras, now_file)
    )
)
now_twin_ras = EmotifiedInstances(
    esi_vec=[
        ESI(
            id=1,
            state_vec=[1260],
            valence=-90.0
        ),
        ESI(
            id=2,
            state_vec=[600],
            valence=90.0
        ),
    ]
)
incentive_file = "incentive"
incentive_twin_config = Twin(
    display_name="Incentive",
    module_id="incentive",
    physical_twin_type="sensor",
    shape=1,
    db_config=DB(
        uri=db_url,
        table="incentive"
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
        log_file="/tmp/%s.log" % incentive_file
    ),
    ras_config=RAS(
        upsert_from="json",
        file_path="%s/%s_ras.json" % (path_ras, incentive_file)
    ),
    broker_config=Broker(
        url=kafka_url,
        sub_topic="incentive_sub",
        pub_topic="",
        group="gwp_sensor",
        auto_offset_reset="latest"
    ),
)
incentive_twin_ras = EmotifiedInstances(
    esi_vec=[
        ESI(
            id=1,
            state_vec=[1260],
            valence=-90.0
        ),
        ESI(
            id=1,
            state_vec=[600],
            valence=90.0
        ),
    ]
)
aggregate_file = "gwp_aggregate"
aggregate_config = Twin(
    display_name="GWP_Aggregate",
    module_id="gwp_aggregate",
    shape=6149,
    sync_rate="1s",
    physical_twin_type="sensor",
    duration_threshold="5s",
    in_twins=[
        date_twin_config,
        quarter_twin_config,
        department_twin_config,
        day_twin_config,
        team_twin_config,
        smv_twin_config,
        wip_twin_config,
        now_twin_config,
        incentive_twin_config
    ],
    db_config=DB(
        table="gwp_aggregate",
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
actual_prod_file = "actual_prod"
actual_prod_twin_config = Twin(
    display_name="Actual Productivity",
    module_id="actual_prod",
    physical_twin_type="sensor",
    shape=1,
    db_config=DB(
        uri=db_url,
        table="actual_prod"
    ),
    in_twins=[aggregate_config],
    vse_config=VSE(
        vse_url=vse_env,
        hnsw_config=HNSW(),
        optimizer_config=Optimizer(),
        shard_number=None,
        wal_config=WAL()
    ),
    log_config=Log(
        level="info",
        log_file="/tmp/%s.log" % actual_prod_file
    ),
    ras_config=RAS(
        upsert_from="json",
        file_path="%s/%s_ras.json" % (path_ras, actual_prod_file)
    )
)
actual_prod_twin_ras = EmotifiedInstances(
    esi_vec=[
        ESI(
            id=1,
            state_vec=[1260],
            valence=-90.0
        ),
        ESI(
            id=1,
            state_vec=[600],
            valence=90.0
        ),
    ]
)
record_file = "gwp_record"
gwp_record_config = Twin(
    display_name="GWP_Record",
    module_id="gwp_record",
    sync_rate="1s",
    shape=6150,
    physical_twin_type="sensor",
    duration_threshold="5s",
    in_twins=[
        aggregate_config,
        actual_prod_twin_config
    ],
    db_config=DB(
        table="gwp_record",
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
        log_file="/tmp/%s.log" % record_file
    )
)
twin_configs = [
    date_twin_config,
    quarter_twin_config,
    department_twin_config,
    day_twin_config,
    team_twin_config,
    smv_twin_config,
    wip_twin_config,
    now_twin_config,
    incentive_twin_config,
    aggregate_config,
    actual_prod_twin_config,
    gwp_record_config
]

core_pp_file = "gwp_corepp"
core_pp = Cortex(
    name="gwp_core",
    pag=aggregate_config.module_id,
    recall=20,
    range=20,
    sync_once=False,
    sync_rate="500ms",
    duration_threshold="1s",
    twin_configs=twin_configs,
    db_config=DB(
        table="gwp_core",
        uri=db_url
    ),
    log_config=Log(
        level="info",
        log_file="/tmp/%s.log" % core_pp_file
    )
)
core_res_file = "gwp_core_res"
core_respond = Cortex(
    name="gwp_core",
    pag=aggregate_config.module_id,
    recall=20,
    range=20,
    sync_once=False,
    sync_rate="200ms",
    duration_threshold="2s",
    twin_configs=twin_configs,
    db_config=DB(
        table="gwp_core",
        uri=db_url
    ),
    log_config=Log(
        level="info",
        log_file="/tmp/%s.log" % core_res_file
    )
)
core_us_file = "gwp_core_us"
core_us = Cortex(
    name="gwp_core",
    pag=aggregate_config.module_id,
    recall=20,
    range=20,
    sync_once=False,
    sync_rate="100ms",
    duration_threshold="2s",
    twin_configs=twin_configs,
    db_config=DB(
        table="gwp_core",
        uri=db_url
    ),
    log_config=Log(
        level="info",
        log_file="/tmp/%s.log" % core_us_file
    )
)
document_file = "gwp_docs"
document_config = Document(
    name="gwp_docs",
    sync_rate="50ms",
    create_n_embed=True,
    twin_config=aggregate_config,
    db_config=DB(
        table="gwp_docs",
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
server_file = "gwp_server"
server_config = WebAPI(
    cortex_config=core_pp,
    user_config=User(
        username=username,
        password=password,
        api_key=api_key,
        db_config=DB(
            table="gwp_users",
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
    '''Date'''
    date_twin_config = TwinConfig(
        twin=date_twin_config
    )
    date_twin_config.to_json_file(
        "%s/%s.json" % (path_twins, date_file))

    '''Quarter'''
    quarter_twin_config = TwinConfig(
        twin=quarter_twin_config
    )
    quarter_twin_config.to_json_file(
        "%s/%s.json" % (path_twins, quarter_file))

    '''Department'''
    department_twin_config = TwinConfig(
        twin=department_twin_config
    )
    department_twin_config.to_json_file("%s/%s.json" % (path_twins, department_file))

    '''Team'''
    team_twin_config = TwinConfig(
        twin=team_twin_config
    )
    team_twin_ras = EmotifiedInstancesConfig(
        emotified_instances=team_twin_ras
    )
    team_twin_ras.to_json_file(
        "%s/%s_ras.json" % (path_ras, team_file))
    team_twin_config.to_json_file(
        "%s/%s.json" % (path_twins, team_file))

    '''Day'''
    day_twin_config = TwinConfig(
        twin=day_twin_config
    )
    day_twin_config.to_json_file(
        "%s/%s.json" % (path_twins, day_file))

    '''Targeted Productivity'''
    targeted_prod_twin_config = TwinConfig(
        twin=targeted_prod_twin_config
    )
    targeted_productivity_twin_ras = EmotifiedInstancesConfig(
        emotified_instances=targeted_productivity_twin_ras
    )
    targeted_productivity_twin_ras.to_json_file(
        "%s/%s_ras.json" % (path_ras, targ_prod_file)
    )
    targeted_prod_twin_config.to_json_file(
        "%s/%s.json" % (path_twins, targ_prod_file)
    )

    '''SMV'''
    smv_twin_config = TwinConfig(
        twin=smv_twin_config
    )
    smv_twin_ras = EmotifiedInstancesConfig(
        emotified_instances=smv_twin_ras
    )
    smv_twin_ras.to_json_file(
        "%s/%s_ras.json" % (path_ras, smv_file)
    )
    smv_twin_config.to_json_file(
        "%s/%s.json" % (path_twins, smv_file)
    )

    '''WIP'''
    wip_twin_config = TwinConfig(
        twin=wip_twin_config
    )
    wip_twin_ras = EmotifiedInstancesConfig(
        emotified_instances=wip_twin_ras
    )
    wip_twin_ras.to_json_file(
        "%s/%s_ras.json" % (path_ras, wip_file)
    )
    wip_twin_config.to_json_file(
        "%s/%s.json" % (path_twins, wip_file)
    )

    '''Overtime'''
    overtime_twin_config = TwinConfig(
        twin=overtime_twin_config
    )
    overtime_twin_ras = EmotifiedInstancesConfig(
        emotified_instances=overtime_twin_ras
    )
    overtime_twin_ras.to_json_file(
        "%s/%s_ras.json" % (path_ras, overtime_file)
    )
    overtime_twin_config.to_json_file(
        "%s/%s.json" % (path_twins, overtime_file)
    )

    '''NOW'''
    now_twin_config = TwinConfig(
        twin=now_twin_config
    )
    now_twin_ras = EmotifiedInstancesConfig(
        emotified_instances=now_twin_ras
    )
    now_twin_ras.to_json_file(
        "%s/%s_ras.json" % (path_ras, now_file)
    )
    now_twin_config.to_json_file(
        "%s/%s.json" % (path_twins, now_file)
    )

    '''Incentive'''
    incentive_twin_config = TwinConfig(
        twin=incentive_twin_config
    )
    incentive_twin_ras = EmotifiedInstancesConfig(
        emotified_instances=incentive_twin_ras
    )
    incentive_twin_ras.to_json_file(
        "%s/%s_ras.json" % (path_ras, incentive_file)
    )
    incentive_twin_config.to_json_file(
        "%s/%s.json" % (path_twins, incentive_file)
    )

    '''Actual Prod'''
    actual_prod_twin_config = TwinConfig(
        twin=actual_prod_twin_config
    )
    actual_prod_twin_ras = EmotifiedInstancesConfig(
        emotified_instances=actual_prod_twin_ras
    )
    incentive_twin_ras.to_json_file(
        "%s/%s_ras.json" % (path_ras, actual_prod_file)
    )
    incentive_twin_config.to_json_file(
        "%s/%s.json" % (path_twins, actual_prod_file)
    )

    '''GWP Aggregate'''
    aggregate_config = TwinConfig(
        twin=aggregate_config
    )
    aggregate_config.to_json_file("%s/%s.json" % (path_twins, aggregate_file))

    '''GWP Record'''
    gwp_record_config = TwinConfig(
        twin=gwp_record_config
    )
    gwp_record_config.to_json_file("%s/%s.json" % (path_twins, record_file))

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
