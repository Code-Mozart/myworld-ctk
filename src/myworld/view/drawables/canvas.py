from src.myworld.util.pygame_compatability import as_hex
from src.myworld.view.drawables.drawable import Drawable
from src.myworld.view.drawables.stylesheet import Stylesheet
from src.myworld.view.primitives.primitive import Primitive, Oval


class Canvas:
    stylesheet: Stylesheet | None = None
    _widget: "Viewport"
    _drawables: dict[any, Drawable] = {}

    def __init__(self, widget: "Viewport", stylesheet: Stylesheet | None = None):
        self.stylesheet = stylesheet
        self._widget = widget

    def add(self, drawable: Drawable):
        self._drawables[drawable.content] = drawable
        self._draw(drawable)

    def get_style(self, drawable: Drawable):
        if self.stylesheet is None:
            return None
        return self.stylesheet.style_for(drawable)

    def redraw(self):
        for drawable in self._drawables.values():
            self._draw(drawable)

    def _draw(self, drawable: Drawable):
        drawable.draw(self._widget.camera, style=self.get_style(drawable))
        for primitive in drawable.primitives:
            self._draw_primitive(primitive)

    def _draw_primitive(self, primitive: Primitive):
        if type(primitive) == Oval:
            self._draw_oval(primitive)
        else:
            raise ValueError(f"Drawing primitive of type {type(primitive)} is not supported.")

    def _draw_oval(self, oval: Oval):
        common_args = [oval.x, oval.y, oval.x + oval.width, oval.y + oval.height]
        fill_color = as_hex(oval.color)
        if oval.canvas_id is None:
            oval.canvas_id = self._widget.create_oval(
                *common_args,
                fill=fill_color,
            )
        else:
            self._widget.coords(
                oval.canvas_id,
                *common_args,
            )
            self._widget.itemconfig(oval.canvas_id, fill=fill_color)
