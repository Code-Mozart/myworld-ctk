from pydantic import BaseModel
from pygame.math import Vector2


class Node(BaseModel):
    position: Vector2
