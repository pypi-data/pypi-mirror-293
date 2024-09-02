from .state import (
    State,
    Side,
    SideConditions,
    Pokemon,
    Move,
)

# noinspection PyUnresolvedReferences
from ._poke_engine import (
    mcts as _mcts,
)


def get_all_options(state: State) -> (list[str], list[str]):
    return [], []


def generate_instructions(state: State, side_one_move: str, side_two_move: str):
    print(f"Ran my function")


def monte_carlo_tree_search(state: State, duration_ms: int = 1000) -> str:
    s = state._into_rust_obj()
    return _mcts(s, duration_ms)


# def generate_instructions(state: State, side_one_move: str, side_two_move: str):
#     s = state._into_rust_obj()
#     instructions = _gi(s, side_one_move, side_two_move)
#     return instructions
