from customtkinter import CTkCanvas

from src.myworld.math2d import Vector2
from src.myworld.view.viewport.camera import Camera


class Viewport(CTkCanvas):
    _camera: Camera

    pan_speed = 1.0
    zoom_speed = 0.1

    #: PUBLIC METHODS

    def zoom_on_world_point(self, world_point: Vector2, zoom_factor: float):
        self._camera.set(
            position=(self._camera.position + (world_point * (zoom_factor - 1.0))) / zoom_factor,
            zoom=self._camera.zoom * zoom_factor,
        )
        self._redraw()

    def zoom_on_screen_point(self, screen_point: Vector2, zoom_factor: float):
        new_zoom = self._camera.zoom * zoom_factor
        self._camera.set(
            position=self._camera.position + (
                    ((zoom_factor - 1.0) / new_zoom) * (screen_point - self._camera.viewport_offset)
            ),
            zoom=new_zoom,
        )
        self._redraw()

    #: OVERRIDEN METHODS

    def update(self) -> None:
        self._redraw()
        super().update()

    #: EVENT HANDLERS

    def _on_resize(self, event):
        self._camera.viewport_offset = Vector2(
            x=event.width / 2,
            y=event.height / 2,
        )
        self._redraw()

    def _on_mouse_scroll(self, event):
        zoom_factor = 1.0 + event.delta * self.zoom_speed
        mouse_screen_pos = Vector2(x=event.x, y=event.y)
        self.zoom_on_screen_point(
            screen_point=mouse_screen_pos,
            zoom_factor=zoom_factor,
        )

    def _on_right_mouse_down(self, event):
        self.drag_start_world_pos = self._camera.project_to_world(Vector2(x=event.x, y=event.y))

    def _on_right_mouse_drag(self, event):
        drag_end_world_pos = self._camera.project_to_world(Vector2(x=event.x, y=event.y))
        self._camera.position -= (drag_end_world_pos - self.drag_start_world_pos) * self.pan_speed
        self.drag_start_world_pos = self._camera.project_to_world(Vector2(x=event.x, y=event.y))
        self._redraw()

    #: PRIVATE METHODS

    def __init__(self, master):
        super().__init__(master=master)
        self._camera = Camera()
        self._reset_camera()

        self.bind("<Configure>", self._on_resize)
        self.bind("<MouseWheel>", self._on_mouse_scroll)
        self.bind("<ButtonPress-2>", self._on_right_mouse_down)
        self.bind("<B2-Motion>", self._on_right_mouse_drag)

        self.drag_start_world_pos = None

    def _reset_camera(self):
        self._camera.set(
            position=Vector2.zero(),
            zoom=Vector2.one(),
            viewport_offset=Vector2(
                x=self.winfo_width() / 2,
                y=self.winfo_height() / 2,
            ),
        )

    def _redraw(self):
        pass
