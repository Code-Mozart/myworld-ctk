from src.myworld.model.base_model import BaseModel

from src.myworld.model.material import Material
from src.myworld.model.world import World


class Project(BaseModel):
    world_materials: dict[str, Material]

    worlds: list[World]
