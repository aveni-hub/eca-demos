import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "avenieca-python"))

from avenieca.api.eca import ECA
from avenieca.api.model import (  # noqa: E402
    AbstractionInsert,
    Config,
    ESSInsert,
)


OP_ROTATE_180 = 101
OP_TRANSLATE_RIGHT_1 = 113
CORE_MODULE = "opbind_pp"
SERVER_URI = "http://localhost:2580/v1"


def create_client() -> ECA:
    config = Config(
        uri=SERVER_URI,
        username="default@email.com",
        password="admin",
    )
    return ECA(config)


def load_seed():
    seed_path = Path(__file__).resolve().parent / "seed" / "programmed_story.json"
    return json.loads(seed_path.read_text(encoding="utf-8"))


def insert_ess(eca: ECA, key: str, payload: dict):
    ess, status = eca.ess.create(
        ESSInsert(
            module_id=CORE_MODULE,
            state=payload["state"],
            valence=payload["valence"],
            score=payload["score"],
            context=f"definition:{key}",
        )
    )
    if status not in (200, 201):
        raise RuntimeError(f"ESS create failed for {key}: {status} {ess}")
    return ess


def create_abstraction(eca: ECA, payload: AbstractionInsert, label: str):
    abstraction, status = eca.abstraction.create(payload)
    if status not in (200, 201):
        raise RuntimeError(f"abstraction create failed for {label}: {status} {abstraction}")
    return abstraction


def main():
    eca = create_client()
    seed = load_seed()["seed"]

    ess_by_ref = {}
    for item in seed["definition_ess"]:
        ess_by_ref[item["key"]] = insert_ess(eca, item["key"], item)

    abstractions = {}
    for item in seed["abstractions"]:
        definition = ess_by_ref[item["definition_ref"]]
        abstraction = create_abstraction(
            eca,
            AbstractionInsert(
                module_id=CORE_MODULE,
                definition=definition.id,
                operator=item["operator"]
                if isinstance(item["operator"], int)
                else {
                    "rotate_180": OP_ROTATE_180,
                    "translate_right_1": OP_TRANSLATE_RIGHT_1,
                }[item["operator"]],
                pattern_id=[abstractions[ref].id for ref in item.get("pattern_refs", [])],
                sequence=[abstractions[ref].id for ref in item.get("sequence_refs", [])],
                score=item["score"],
                valence=item["valence"],
            ),
            item["key"],
        )
        abstractions[item["key"]] = abstraction

    for item in seed.get("bindings", []):
        abstraction = abstractions[item["abstraction_ref"]]
        ess = ess_by_ref[item["ess_ref"]]
        _, status = eca.abstraction.bind_to_ess(CORE_MODULE, abstraction.id, ess.id)
        if status not in (200, 201):
            raise RuntimeError(
                f"binding create failed for {item['abstraction_ref']} -> {item['ess_ref']}: {status}"
            )

    print("seeded operator-binding abstractions via API")
    print(f"  definition ess: {len(seed['definition_ess'])}")
    print(f"  abstractions: {len(abstractions)}")
    print(f"  bindings: {len(seed.get('bindings', []))}")
    print("  manual goals: 0")
    print("  note: root goal and subgoals should now be created by the reasoning loop")


if __name__ == "__main__":
    main()
