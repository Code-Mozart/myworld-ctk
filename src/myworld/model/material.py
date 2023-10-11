from src.myworld.model.base_model import BaseModel
from pygame import Color


class Material(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    color: Color
