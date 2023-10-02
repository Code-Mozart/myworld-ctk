from customtkinter import CTkCanvas

from src.myworld.math2d import Vector2
from src.myworld.model.world import World
from src.myworld.util.pygame_compatability import as_hex
from src.myworld.view.viewport.camera import Camera
from src.myworld.view.viewport.viewport import Viewport

NO_WORLD_BG_COLOR = "#202020"


class WorldViewport(Viewport):
    _world: World | None = None

    node_radius = 5

    def __init__(self, master):
        super().__init__(master=master)
        self.configure(bg=NO_WORLD_BG_COLOR)

    @property
    def world(self) -> World | None:
        return self._world

    @world.setter
    def world(self, value: World | None):
        self._world = value
        self._reset_camera()
        self._redraw()

    def _redraw(self):
        # TODO: move elements instead of destroying and recreating them

        self.delete("all")
        if self.world is None:
            self.configure(bg=NO_WORLD_BG_COLOR)
            return

        self._draw_nodes()

        self.configure(bg=as_hex(self.world.material.color))

    def _draw_nodes(self):
        for node in self.world.nodes:
            pos = self._camera.project_to_screen(node.position)
            self.create_oval(
                pos.x - self.node_radius,
                pos.y - self.node_radius,
                pos.x + self.node_radius,
                pos.y + self.node_radius,
                fill="#ffffff",
            )
