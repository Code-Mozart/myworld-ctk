from src.myworld.model.world import World
from src.myworld.util.pygame_compatability import as_hex
from src.myworld.view.drawables.default.node import DrawableNode
from src.myworld.view.drawables.default.stylesheet import DefaultStylesheet
from src.myworld.view.viewport.viewport import Viewport

NO_WORLD_BG_COLOR = "#202020"


class WorldViewport(Viewport):
    _world: World | None = None

    def __init__(self, master):
        super().__init__(master=master)
        self._canvas.stylesheet = DefaultStylesheet(
            node_style=DrawableNode.Style()
        )
        self.configure(bg=NO_WORLD_BG_COLOR)

    @property
    def world(self) -> World | None:
        return self._world

    @world.setter
    def world(self, value: World | None):
        self._world = value

        # TODO: remove all old drawables from the canvas

        # TODO: add all new drawables to the canvas
        for node in self._world.nodes:
            self.add_node(node)
        self.configure(bg=as_hex(self._world.material.color))

        self._reset_camera()
        self._redraw()

    def add_node(self, node):
        self._canvas.add(DrawableNode(node))
