from src.myworld.model.base_model import BaseModel
from pygame import Color


class PositionComponent(BaseModel):
    x: float
    y: float


class RectSizeComponent(BaseModel):
    width: float
    height: float


class ColorComponent(BaseModel):
    color: Color
