from typing import Tuple, List

from gojos import repo, model

def save(graph_names: List = None, val: Tuple = None) -> Tuple:
    repo.save(graph_names)
    return val


def graph():
    return repo.graph()
