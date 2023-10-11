from src.myworld.view.drawables.default.node import DrawableNode
from src.myworld.view.drawables.drawable import Drawable
from src.myworld.view.drawables.stylesheet import Stylesheet


class DefaultStylesheet(Stylesheet):
    node_style: DrawableNode.Style

    def style_for(self, drawable: Drawable):
        _STYLE_MAP = {
            DrawableNode: self.node_style,
        }
        return _STYLE_MAP[type(drawable)]
