from customtkinter import CTkCanvas

from src.myworld.math2d import Vector2
from src.myworld.model.world import World
from src.myworld.util.pygame_compatability import as_hex
from src.myworld.view.viewport.camera import Camera

NO_WORLD_BG_COLOR = "#202020"


class WorldViewport(CTkCanvas):
    _world: World | None = None
    _camera: Camera

    node_radius = 5

    def __init__(self, master):
        super().__init__(master=master)
        self._camera = Camera()
        self.configure(bg=NO_WORLD_BG_COLOR)
        self._reset_camera()

        self.bind("<Configure>", self._on_resize)
        self.bind("<ButtonPress-2>", self._on_mouse_down)
        self.bind("<B2-Motion>", self._on_mouse_drag)

        self.drag_start_world_pos = None

    def update(self) -> None:
        self._redraw()
        super().update()

    @property
    def world(self) -> World | None:
        return self._world

    @world.setter
    def world(self, value: World | None):
        self._world = value
        self._reset_camera()
        self._redraw()

    def _on_mouse_down(self, event):
        self.drag_start_world_pos = self._camera.project_to_world(Vector2(x=event.x, y=event.y))

    def _on_mouse_drag(self, event):
        drag_end_world_pos = self._camera.project_to_world(Vector2(x=event.x, y=event.y))
        self._camera.position += drag_end_world_pos - self.drag_start_world_pos
        self.drag_start_world_pos = self._camera.project_to_world(Vector2(x=event.x, y=event.y))

        self._redraw()

    def _reset_camera(self):
        self._camera.set(
            position=Vector2.zero(),
            zoom=Vector2.one(),
            viewport_offset=Vector2(
                x=self.winfo_width() / 2,
                y=self.winfo_height() / 2,
            ),
        )

    def _on_resize(self, event):
        self._camera.viewport_offset = Vector2(
            x=self.winfo_width() / 2,
            y=self.winfo_height() / 2,
        )
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
            pos = self._camera.project_to_world(node.position)
            self.create_oval(
                pos.x - self.node_radius,
                pos.y - self.node_radius,
                pos.x + self.node_radius,
                pos.y + self.node_radius,
                fill="#ffffff",
            )
