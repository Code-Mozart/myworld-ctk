from pydantic import BaseModel

from src.myworld.model.material import Material


class World(BaseModel):
    name: str | None = None
    material: Material
