import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "avenieca-python"))

from avenieca.api.eca import ECA  # noqa: E402
from avenieca.api.model import Config  # noqa: E402


CORE_MODULE = "autoabs_aa"
SERVER_URI = "http://localhost:2580/v1"


def create_client() -> ECA:
    config = Config(
        uri=SERVER_URI,
        username="default@email.com",
        password="admin",
    )
    return ECA(config)


def format_operator(op: int) -> str:
    return {
        -1: "sequence",
        101: "rotate_180",
        113: "translate_right_1",
    }.get(op, str(op))


def main():
    eca = create_client()
    abstractions, _ = eca.abstraction.get_all(CORE_MODULE)
    attention, _ = eca.ess.get_all_sequence(CORE_MODULE)
    goal_stack, _ = eca.goal.get_stack(CORE_MODULE)

    print("auto-abstraction API inspection")
    print(f"  abstraction count: {len(abstractions) if abstractions else 0}")
    if abstractions:
        for abstraction in abstractions:
            print(
                f"  abstraction id={abstraction.id} definition={abstraction.definition} "
                f"operator={format_operator(abstraction.operator)} sequence={abstraction.sequence} "
                f"score={abstraction.score}"
            )

    print(f"  attention sequence count: {len(attention) if attention else 0}")
    if attention:
        latest = attention[0]
        print(f"  latest attention ess id={latest.id} context={latest.context} state={latest.state}")

    print(f"  goal stack count: {len(goal_stack) if goal_stack else 0}")
    if goal_stack:
        for goal in goal_stack:
            print(
                f"  goal id={goal.id} abstraction={goal.abstraction} parent={goal.parent} "
                f"stage={goal.stage} status={goal.status}"
            )


if __name__ == "__main__":
    main()
