from src.myworld.model.base_model import BaseModel

from src.myworld.math2d import Vector2


class Node(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    id: int
    position: Vector2

    def __hash__(self):
        return self.id
