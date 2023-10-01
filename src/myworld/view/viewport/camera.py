from src.myworld.math2d import Transform2, Vector2


class Camera:
    transform: Transform2 = Transform2.identity()
    """The transform that converts screen coordinates to world coordinates."""
    
    _inverse: Transform2 = Transform2.identity()
    """The inverse of the transform that converts world coordinates to screen coordinates."""

    _position: Vector2 = Vector2.zero()
    _zoom: Vector2 = Vector2.one()
    _viewport_offset: Vector2 = Vector2.zero()

    def project_to_screen(self, world_point) -> Vector2:
        return self._inverse.multiply(world_point)

    def project_to_world(self, screen_point) -> Vector2:
        return self.transform.multiply(screen_point)

    def __init__(self, position: Vector2 = None, zoom: Vector2 = None, viewport_offset: Vector2 = None):
        self.set(position, zoom, viewport_offset)

    def set(self, position: Vector2 | None = None, zoom: Vector2 | None = None, viewport_offset: Vector2 | None = None):
        # not calling setters to avoid recalculating transform thrice
        if position is not None:
            self._position = position
        if zoom is not None:
            self._zoom = zoom
        if viewport_offset is not None:
            self._viewport_offset = viewport_offset
        self.recalculate_transform()

    def recalculate_transform(self) -> Transform2:
        self.transform = Transform2(
            translation=((-self.viewport_offset / self.zoom) + self.position)[0:2],
            scale=(1.0 / self.zoom)[0:2],
        )
        self._inverse = self.transform.inverse()
        return self.transform

    @property
    def position(self) -> Vector2:
        return self._position

    @position.setter
    def position(self, value: Vector2):
        self._position = value
        self.recalculate_transform()

    @property
    def zoom(self) -> Vector2:
        return self._zoom

    @zoom.setter
    def zoom(self, value):
        self._zoom = value
        self.recalculate_transform()

    @property
    def viewport_offset(self) -> Vector2:
        return self._viewport_offset

    @viewport_offset.setter
    def viewport_offset(self, value: Vector2):
        self._viewport_offset = value
        self.recalculate_transform()
