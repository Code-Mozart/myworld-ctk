from src.myworld.math2d import Vector2
from src.myworld.model.node import Node


def load_node_from_tuple(node_tuple):
    if len(node_tuple) != 3:
        raise ValueError("Node tuple must have 3 elements: (id, x, y)")
    return Node(
        id=node_tuple[0],
        position=Vector2(node_tuple[1:3]),
    )
