from pprint import pprint

import avenieca.config.twin
from avenieca.api.model import *
from avenieca.api.eca import ECA

config = Config(uri="http://localhost:2580/v1", username="default@email.com", password="admin")

eca = ECA(config)

aggregate = ESSInsert(
    module_id="aggregate001",
    state=[],
    valence=10.0,
    avg_ess_valence=15.0,
    score=4,
    total_ess_score=15,
    avg_ess_score=5,
    aggregate_id=[2, 3],
    aggregate_valence=[15, 15],
    aggregate_score=[10],
    aggregate_module_id=["camera1", "heat_reader"],
    aggregate_shape=[2, 3],
    aggregate_context=[None, None],
    aggregate_emb_inp=[None, None],
    context=None,
)

'''Aggregates'''
# res, status = eca.aggregate.create(data=aggregate)
# res, status = eca.aggregate.get_all(module_id="aggregate001")
# res, status = eca.aggregate.get_one(module_id="aggregate001", db_id=3)
# res, status = eca.aggregate.get_one_sequence(module_id="aggregate001", sequence_id=3)
# res, status = eca.aggregate.get_all_sequence(module_id="aggregate001")
# res, status = eca.aggregate.get_one_pretty(module_id="aggregate001", db_id=3)
# res, status = eca.aggregate.delete(module_id="aggregate001", db_id=34)
# res, status = eca.aggregate.search(data=Search(
#     module_id="aggregate001",
#     state=[25.0, 18.0, 2.0, 2.0, 19.0],
#     limit=1
# ))

'''ESS'''
ess = ESSInsert(
    module_id="air_conditioner",
    state=[11],
    valence=10.0,
    score=4,
    embedding_input=1,
    context=None,
)
# res, status = eca.ess.create(data=ess)
# res, status = eca.ess.get_all(module_id="air_conditioner")
# res, status = eca.ess.get_one(module_id="air_conditioner", db_id=8)
# res, status = eca.ess.update(module_id="air_conditioner", db_id=8, data=ess)
# res, status = eca.ess.get_one_sequence(module_id="air_conditioner", sequence_id=3)
# res, status = eca.ess.get_all_sequence(module_id="air_conditioner")
# res, status = eca.ess.get_one_pretty(module_id="gwp_record", db_id=1)
# res, status = eca.ess.search(data=Search(
#     module_id="air_conditioner",
#     state=[18],
#     limit=1
# ))
# res, status = eca.ess.get_one_embedding(module_id="air_conditioner", embedding_input=1)
# res, status = eca.ess.get_all_aggregates(module_id="team", aggregate_module_id="gwp_aggregate", ess_id=1)

'''Sequence'''
sequence = SequenceInsert(
    module_id="air_conditioner",
    instance_id=10,
    status="e",
    context=None,
)
# res, status = eca.sequence.create(data=sequence)
# res, status = eca.sequence.get_one(module_id="air_conditioner", db_id=4)
# res, status = eca.sequence.get_all(module_id="air_conditioner")
# res, status = eca.sequence.update(module_id="air_conditioner", db_id=4, data=sequence)
# res, status = eca.sequence.delete(module_id="aggregate001", db_id=59)
# res, status = eca.sequence.delete(module_id="aggregate001", db_id=58)
# res, status = eca.sequence.delete(module_id="aggregate001", db_id=39)
# res, status = eca.sequence.delete(module_id="aggregate001", db_id=38)
# res, status = eca.sequence.delete(module_id="aggregate001", db_id=53)
# res, status = eca.sequence.delete(module_id="aggregate001", db_id=52)
# res, status = eca.sequence.delete(module_id="aggregate001", db_id=50)
# res, status = eca.sequence.delete(module_id="aggregate001", db_id=49)
# res, status = eca.sequence.delete(module_id="aggregate001", db_id=48)
# res, status = eca.sequence.delete(module_id="aggregate001", db_id=47)
# res, status = eca.sequence.delete(module_id="aggregate001", db_id=46)
# res, status = eca.sequence.delete(module_id="aggregate001", db_id=45)
# res, status = eca.sequence.delete(module_id="aggregate001", db_id=44)
# res, status = eca.sequence.delete(module_id="aggregate001", db_id=43)
# res, status = eca.sequence.delete(module_id="aggregate001", db_id=42)
# res, status = eca.sequence.delete(module_id="aggregate001", db_id=41)
# res, status = eca.sequence.delete(module_id="aggregate001", db_id=40)

nsr = NextStateRequest(
    module_id="aggregate001",
    recall=20,
    range=20,
    n=1,
    status="e"
)
# res, status = eca.cortex.predictions(data=nsr)
# res, status = eca.cortex.predictions_raw(data=nsr)

'''Document'''
document = DocumentInsert(
    doc_id="001",
    text="testing 123",
    embed=True,
)

# res, status = eca.document.create(data=document)
# res, status = eca.document.get_one(db_id=20)
# res, status = eca.document.get_all()
# res, status = eca.document.update(db_id=20, data=document)
# res, status = eca.document.delete(db_id=100)

'''Embedding'''
input_hash = avenieca.encode("my_secret", "the inputs")
embedding = EmbeddingInputInsert(
    module_id="air_conditioner",
    input="the inputs",
    hash=input_hash
)

# res, status = eca.embedding.create(data=embedding)
# res, status = eca.embedding.get_one(module_id="air_conditioner", db_id=1)
# res, status = eca.embedding.get_all(module_id="air_conditioner")
# res, status = eca.embedding.update(module_id="air_conditioner", db_id=1, data=embedding)
# res, status = eca.embedding.delete(module_id="air_conditioner", db_id=1)

'''Response'''
# res, status = eca.response.get_one(db_id=100)
# res, status = eca.response.get_all()

'''Retrieval'''
retrieval = RetrievalRequest(
    query="what is the temperature on 3rd of may at around 1pm?"
)
# res, status = eca.retrieval.query(data=retrieval)

'''create ess, then create aggregate'''
ess_temperature = ESSResponse(
    id=2,
    created_at='',
    updated_at='',
    module_id="temperature",
    state=[28.0],
    valence=-90,
    score=1,
    context=None,
    embedding_input=None
)
ess_air_conditioner = ESSResponse(
    id=5,
    created_at='',
    updated_at='',
    state=[25.0],
    module_id='air_conditioner',
    valence=90.0,
    score=18,
    embedding_input=None,
    context=None
)
ess_occupancy = ESSResponse(
    id=7,
    created_at='',
    updated_at='',
    state=[10.0],
    module_id='occupancy',
    valence=-90.0,
    score=6,
    embedding_input=None,
    context=None
)
ess_purifier = ESSResponse(
    id=3,
    state=[2.0],
    module_id='purifier',
    valence=90.0,
    score=28,
    embedding_input=None,
    context=None)
ess_air_quality_index = ESSResponse(
    id=6,
    created_at='',
    updated_at='',
    state=[70.0],
    module_id='air_quality_index',
    valence=-90.0,
    score=2,
    embedding_input=None,
    context=None
)
aggregate_insert = ESSInsert(
    module_id="aggregate001",
    state=[],
    valence=10.0,
    avg_ess_valence=0.0,
    score=0,
    total_ess_score=0,
    avg_ess_score=0,
    aggregate_id=[],
    aggregate_valence=[],
    aggregate_score=[],
    aggregate_module_id=[],
    aggregate_shape=[],
    aggregate_context=[],
    aggregate_emb_inp=[],
    context=None,
)


def create_aggregate_from_ess(array_ess: List[ESSResponse], aggregate_insert: ESSInsert):
    total_ess_score = 0
    total_ess_valence = 0.0
    for ess in array_ess:
        aggregate_insert.state.extend(ess.state)
        aggregate_insert.aggregate_module_id.append(ess.module_id)
        aggregate_insert.aggregate_id.append(ess.id)
        aggregate_insert.aggregate_context.append(ess.context)
        aggregate_insert.aggregate_valence.append(ess.valence)
        aggregate_insert.aggregate_score.append(ess.score)
        aggregate_insert.aggregate_emb_inp.append(ess.embedding_input)
        aggregate_insert.aggregate_shape.append(len(ess.state))
        total_ess_score += ess.score
        total_ess_valence += ess.valence
    aggregate_insert.total_ess_score = total_ess_score
    aggregate_insert.avg_ess_score = int(total_ess_score / len(array_ess))
    aggregate_insert.avg_ess_valence = total_ess_valence / len(array_ess)
    aggregate_insert.valence = total_ess_valence
    return aggregate_insert


# ess_in = ESSInsert(
#     module_id="air_quality_index",
#     state=[90.0],
#     valence=-90,
#     score=1,
#     context=None,
#     embedding_input=None
# )
# res, status = eca.ess.create(data=ess_in)

agg_in = create_aggregate_from_ess(
    [
        ess_air_conditioner,
        ess_air_quality_index,
        ess_occupancy,
        ess_purifier,
        ess_temperature
    ],
    aggregate_insert)

# res, status = eca.ess.create(data=agg_in)
# res, status = eca.aggregate.upsert(module_id="aggregate001", db_id=5)

# res, status = eca.sequence.create(data=SequenceInsert(
#     module_id="aggregate001",
#     instance_id=34,
#     status="sk"
# ))

# res, status = eca.sequence.get_one(module_id="aggregate001", db_id=37)

# res, status = eca.ess.search(data=Search(
#     module_id="purifier",
#     state=[2.0],
#     limit=3
# ))

nsr = NextStateRequest(
    module_id="aggregate001",
    recall=3,
    range=2,
    n=1,
    current_state=33,
    previous_state=[32, 31]
)
res, status = eca.cortex.predictions_raw(data=nsr)

try:
    pprint(res.__dict__)
except:
    print(len(res))
print(status)
