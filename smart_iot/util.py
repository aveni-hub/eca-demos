from avenieca.api.model import *


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
