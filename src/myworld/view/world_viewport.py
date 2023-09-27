from customtkinter import CTkCanvas

from src.myworld.model.world import World
from src.myworld.util.pygame_compatability import as_hex

NO_WORLD_BG_COLOR = "#202020"


class WorldViewport(CTkCanvas):
    world: World

    def __init__(self, master):
        super().__init__(master=master)

    def update(self) -> None:
        self._redraw()
        super().update()

    def _redraw(self):
        if self.world is None:
            self.configure(bg=NO_WORLD_BG_COLOR)

        self.configure(bg=as_hex(self.world.material.color))
