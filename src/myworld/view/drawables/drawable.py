from typing import Optional

from pygame import Color

from src.myworld.math2d import Vector2
from src.myworld.util.kwargs_helper import exactly_one_of, maybe
from src.myworld.view.primitives.primitive import Primitive, Oval


class Drawable:
    primitives: list[Primitive] = []
    _content: any
    __current_draw_index: int = 0
    __camera: Optional["Camera"] = None

    def __init__(self, *args):
        self._content = args if len(args) > 1 else args[0]

    @property
    def content(self):
        return self._content

    def draw(self, camera: "Camera", **kwargs):
        self._prepare(camera)
        if type(self._content) == list:
            self._draw(*self._content, **kwargs)
        elif type(self._content) == dict:
            self._draw(**self._content, **kwargs)
        else:
            self._draw(self._content, **kwargs)

    def _draw(self, *args, **kwargs):
        pass

    def _prepare(self, camera):
        self.__current_draw_index = 0
        self.__camera = camera

    #: DRAW METHODS

    def filled_circle(
            self,
            world_pos: Vector2 = ...,
            world_radius: float = ...,
            fill_color: Color = ...,
            screen_pos: Vector2 = ...,
            screen_radius: float = ...
    ):
        """
        Draws a filled circle on the canvas.

        :param world_pos:
            The position of the circle's center in world coordinates. Mutually exclusive with parameter screen_pos.
        :param world_radius:
            The radius of the circle in world coordinates. Mutually exclusive with parameter screen_radius.
        :param fill_color:
            The color of the circle's fill.
        :param screen_pos:
            The position of the circle's center in screen coordinates. Mutually exclusive with parameter world_pos.
        :param screen_radius:
            The radius of the circle in screen coordinates. Mutually exclusive with parameter world_radius.
        """

        kwargs = {
            "world_pos": world_pos,
            "fill_color": fill_color,
            "screen_pos": screen_pos,
        }

        if world_radius is not ...:
            kwargs["world_width"] = world_radius * 2.0
            kwargs["world_height"] = world_radius * 2.0
        elif screen_radius is not ...:
            kwargs["screen_width"] = screen_radius * 2.0
            kwargs["screen_height"] = screen_radius * 2.0

        self.filled_oval(**kwargs)

    def filled_oval(
            self,
            world_pos: Vector2 = ...,
            world_width: float = ...,
            world_height: float = ...,
            fill_color: Color = ...,
            screen_pos: Vector2 = ...,
            screen_width: float = ...,
            screen_height: float = ...,
    ):
        """
        Draws a filled oval on the canvas.

        :param world_pos:
            The position of the oval's center in world coordinates. Mutually exclusive with parameter screen_pos.
        :param world_width:
            The width of the oval in world coordinates. Mutually exclusive with parameter screen_width.
        :param world_height:
            The height of the oval in world coordinates. Mutually exclusive with parameter screen_height.
        :param fill_color:
            The color of the oval's fill.
        :param screen_pos:
            The position of the oval's center in screen coordinates. Mutually exclusive with parameter world_pos.
        :param screen_width:
            The width of the oval in screen coordinates. Mutually exclusive with parameter world_width.
        :param screen_height:
            The height of the oval in screen coordinates. Mutually exclusive with parameter world_height.
        """

        screen_pos = exactly_one_of(
            world_pos=maybe(self.__camera.project_to_screen, world_pos), screen_pos=screen_pos
        )
        screen_width = exactly_one_of(
            world_width=maybe(self.__camera.width_to_screen, world_width), screen_width=screen_width
        )
        screen_height = exactly_one_of(
            world_height=maybe(self.__camera.height_to_screen, world_height), screen_height=screen_height
        )
        fill_color = fill_color or Color("white")

        self.__draw_oval(
            screen_x=screen_pos.x - screen_width / 2.0,
            screen_y=screen_pos.y - screen_height / 2.0,
            screen_width=screen_width,
            screen_height=screen_height,
            fill_color=fill_color,
        )

    #: DRAWING METHODS

    def __draw_oval(
            self,
            screen_x: float,
            screen_y: float,
            screen_width: float,
            screen_height: float,
            fill_color: Color,
    ):
        if self.__is_current_primitive_a(Oval):
            oval = self.__current_primitive()
            oval.x = screen_x
            oval.y = screen_y
            oval.width = screen_width
            oval.height = screen_height
            oval.color = fill_color
        else:
            self.__add_primitive(
                Oval(
                    canvas_id=None,
                    x=screen_x,
                    y=screen_y,
                    width=screen_width,
                    height=screen_height,
                    color=fill_color,
                )
            )

        self.__current_draw_index += 1

    #: PRIMITIVE MANAGEMENT

    def __is_current_primitive_a(self, primitive_type):
        return self.__has_next_primitive() and isinstance(self.__current_primitive(), primitive_type)

    def __has_next_primitive(self):
        return self.__current_draw_index < len(self.primitives)

    def __current_primitive(self):
        return self.primitives[self.__current_draw_index]

    def __add_primitive(self, primitive):
        self.primitives = self.primitives[:self.__current_draw_index]
        self.primitives.append(primitive)
