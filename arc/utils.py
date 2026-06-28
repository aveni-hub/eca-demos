from avenieca.api.model import *
from avenieca.api.eca import ECA
from avenieca.utils import hash

status_created = 201
status_ok = 200
status_not_found = 404


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


def create_ess_and_sequence(eca: ECA, ess_input, secret, twin_config: Twin, embedding_api=None,
                            embedding=False) -> ESSResponse:
    if embedding:
        input_hash = hash.encode(ess_input, secret)
        emb_inp, status = eca.embedding.get_one_with_hash(module_id=twin_config.module_id, data=EmbeddingInputHash(
            hash=input_hash
        ))
        ess_response: ESSResponse
        if status == status_ok and emb_inp:
            emb_inp: EmbeddingInputResponse = emb_inp
            response, status = eca.ess.get_one_with_embedding(module_id=twin_config.module_id, emb_input=emb_inp.id)
            if status == status_ok and response:
                ess: ESSResponse = response
                insert_sequence(eca, SequenceInsert(
                    instance_id=ess.id,
                    module_id=twin_config.module_id,
                    status='e'
                ))
                return ess
            elif status == status_not_found:
                state = embedding_api.Embedding.create(input=ess_input, engine='text-embedding-ada-002')['data'][0][
                    'embedding']
                ess: ESSInsert = ESSInsert(
                    module_id=twin_config.module_id,
                    state=state,
                    valence=50,
                    embedding_input=emb_inp.id
                )
                ess_response = insert_ess(eca, ess)
                if ess.state:
                    insert_sequence(eca, SequenceInsert(
                        instance_id=ess_response.id,
                        module_id=twin_config.module_id,
                        status='e'
                    ))
                    return ess_response
                else:
                    raise Exception("empty state on insert (%s)" % ess.module_id)
            else:
                error: Error = response
                raise Exception(error)
        else:
            state = embedding_api.Embedding.create(input=ess_input, engine='text-embedding-ada-002')['data'][0][
                'embedding']
            response, status = eca.embedding.create(data=EmbeddingInputInsert(
                input=ess_input,
                hash=input_hash,
                module_id=twin_config.module_id
            ))
            if status == status_created:
                emb_inp: EmbeddingInputResponse = response
                ess: ESSInsert = ESSInsert(
                    module_id=twin_config.module_id,
                    state=state,
                    valence=50,
                    embedding_input=emb_inp.id
                )
                ess_response = insert_ess(eca, ess)
                if ess.state:
                    insert_sequence(eca, SequenceInsert(
                        instance_id=ess_response.id,
                        module_id=twin_config.module_id,
                        status='e'
                    ))
                    return ess_response
                else:
                    raise Exception("empty state on insert (%s)" % ess.module_id)
            else:
                error: Error = response
                raise Exception(error)
    else:
        ess = search_insert_ess_and_sequence(eca, ESSInsert(
            module_id=twin_config.module_id,
            state=ess_input,
            valence=50,
        ))
        return ess


def insert_ess(eca: ECA, ess: ESSInsert) -> ESSResponse:
    response, status = eca.ess.create(data=ess)
    if status == status_created and response:
        ess: ESSResponse = response
        return ess
    else:
        raise Exception(response)


def insert_sequence(eca: ECA, sequence: SequenceInsert) -> SequenceResponse:
    response, status = eca.sequence.create(data=sequence)
    if status == status_created and response:
        seq: SequenceResponse = response
        return seq
    else:
        raise Exception(response)


def search_insert_ess_and_sequence(eca, ess_insert: ESSInsert) -> ESSResponse:
    response, status = eca.ess.search(data=Search(
        state=ess_insert.state,
        module_id=ess_insert.module_id,
        limit=1
    ))
    if status == status_ok and response:
        search_results: List[SearchResult] = response
        if search_results[0].score == 0.0:
            ess: ESSResponse = search_results[0].ess
            insert_sequence(eca, SequenceInsert(
                instance_id=ess.id,
                module_id=ess.module_id,
                status='e'
            ))
            return ess
        else:
            ess: ESSResponse = insert_ess(eca, ess_insert)
            if ess.state:
                insert_sequence(eca, SequenceInsert(
                    instance_id=ess.id,
                    module_id=ess.module_id,
                    status='e'
                ))
                return ess
            else:
                raise Exception("empty state on insert (%s)" % ess.module_id)
    else:
        ess: ESSResponse = insert_ess(eca, ess_insert)
        if ess.state:
            insert_sequence(eca, SequenceInsert(
                instance_id=ess.id,
                module_id=ess.module_id,
                status='e'
            ))
            return ess
        else:
            raise Exception("empty state on insert (%s)" % ess.module_id)


def create_embedding_then_insert_ess_and_sequence(eca, ess_input, input_hash, twin_config: Twin,
                                                  embedding_api) -> ESSResponse:
    state = embedding_api.Embedding.create(input=ess_input, engine='text-embedding-ada-002')['data'][0]['embedding']
    response, status = eca.embedding.create(data=EmbeddingInputInsert(
        input=ess_input,
        hash=input_hash,
        module_id=twin_config.module_id
    ))
    if status == status_created:
        emb_inp: EmbeddingInputResponse = response
        ess: ESSInsert = ESSInsert(
            module_id=twin_config.module_id,
            state=state,
            valence=50,
            embedding_input=emb_inp.id
        )
        ess_response = insert_ess(eca, ess)
        if ess.state:
            insert_sequence(eca, SequenceInsert(
                instance_id=ess_response.id,
                module_id=twin_config.module_id,
                status='e'
            ))
            return ess_response
        else:
            raise Exception("empty state on insert (%s)" % ess.module_id)
    else:
        error: Error = response
        raise Exception(error)
