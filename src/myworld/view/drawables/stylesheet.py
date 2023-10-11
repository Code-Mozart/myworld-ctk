from abc import abstractmethod

from src.myworld.model.base_model import BaseModel
from src.myworld.view.drawables.drawable import Drawable


class Stylesheet(BaseModel):
    @abstractmethod
    def style_for(self, drawable: Drawable):
        pass
