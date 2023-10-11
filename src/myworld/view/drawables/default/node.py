from pygame import Color

from src.myworld.model.base_model import BaseModel
from src.myworld.model.node import Node
from src.myworld.view.drawables.drawable import Drawable


class DrawableNode(Drawable):
    class Style(BaseModel):
        node_color: Color = Color("white")
        node_radius: float = 5

    def _draw(self, node: Node, style):
        self.filled_circle(node.position, screen_radius=style.node_radius, fill_color=style.node_color)
