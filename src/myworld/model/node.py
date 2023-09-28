from pydantic import BaseModel
from pygame.math import Vector2


class Node(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    id: int
    position: Vector2
