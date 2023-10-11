from src.myworld.model.base_model import BaseModel

from src.myworld.view.primitives.components import (
    PositionComponent,
    RectSizeComponent,
    ColorComponent,
)


class Primitive(BaseModel):
    canvas_id: int | None


class Oval(Primitive, PositionComponent, RectSizeComponent, ColorComponent):
    pass
