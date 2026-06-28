import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "avenieca-python"))

from avenieca.api.eca import ECA  # noqa: E402
from avenieca.api.model import Config, ESSInsert, SequenceInsert  # noqa: E402


PAG_MODULE = "autoabs_pag"
CORE_MODULE = "autoabs_aa"
SERVER_URI = "http://localhost:2580/v1"


def create_client() -> ECA:
    config = Config(
        uri=SERVER_URI,
        username="default@email.com",
        password="admin",
    )
    return ECA(config)


def main():
    eca = create_client()
    attention, status = eca.ess.get_all_sequence(PAG_MODULE)
    if status != 200:
        raise RuntimeError(f"failed to fetch pag attention: {status} {attention}")
    if not attention:
        raise RuntimeError("no pag attention rows found; stream experience before learning")

    staged = 0
    for offset, ess in enumerate(reversed(attention), start=1):
        staged_ess, status = eca.ess.create(
            ESSInsert(
                module_id=CORE_MODULE,
                state=ess.state,
                index=getattr(ess, "index", []),
                valence=ess.valence,
                score=ess.score,
                context=f"learning_pass:{offset}",
            )
        )
        if status not in (200, 201):
            raise RuntimeError(f"failed to stage ess {ess.id}: {status} {staged_ess}")

        sequence, status = eca.sequence.create(
            SequenceInsert(
                module_id=CORE_MODULE,
                instance_id=staged_ess.id,
                status="p",
                context=f"learning_pass:{offset}",
            )
        )
        if status not in (200, 201):
            raise RuntimeError(
                f"failed to stage sequence for ess {staged_ess.id}: {status} {sequence}"
            )
        staged += 1

    print("staged auto-abstraction learning pass via API")
    print(f"  pag attention rows: {len(attention)}")
    print(f"  staged core-aa sequences: {staged}")


if __name__ == "__main__":
    main()
