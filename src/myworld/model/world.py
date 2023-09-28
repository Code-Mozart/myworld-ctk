from pydantic import BaseModel

from src.myworld.model.material import Material
from src.myworld.model.node import Node


class World(BaseModel):
    name: str | None = None
    material: Material
    nodes: list[Node] = []
