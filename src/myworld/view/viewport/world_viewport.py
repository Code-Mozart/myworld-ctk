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
        # TODO: move elements instead of destroying and recreating them

        self.delete("all")
        if self.world is None:
            self.configure(bg=NO_WORLD_BG_COLOR)

        self._draw_nodes()

        self.configure(bg=as_hex(self.world.material.color))

    def _draw_nodes(self):
        for node in self.world.nodes:
            self.create_oval(
                node.position.x - 5 + self.winfo_screenwidth() / 2,
                node.position.y - 5 + self.winfo_screenheight() / 2,
                node.position.x + 5 + self.winfo_screenwidth() / 2,
                node.position.y + 5 + self.winfo_screenheight() / 2,
                fill="#ffffff",
            )
