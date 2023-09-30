import numpy as _numpy

from src.myworld.math2d import init_helpers


class Vector2(_numpy.ndarray):
    def __new__(cls, *args, x=..., y=...):
        if len(args) == 0:
            if x is ... or y is ...:
                raise ValueError(
                    "When initializing Vector2 with no positional arguments, both x and y must be specified"
                )
            return cls.__from_values(x, y)

        if x is not ... or y is not ...:
            raise ValueError(
                "When initializing Vector2 with positional arguments, no keyword arguments must be specified"
            )
        if len(args) == 1:
            return cls.__from_subscriptable(args[0])
        if len(args) == 2:
            return cls.__from_values(args[0], args[1])

        raise ValueError(
            "Vector2 must be initialized with both and y as positional arguments, both as keyword arguments,"
            "or with an array-like object"
        )

    @classmethod
    def __from_subscriptable(cls, subscriptable):
        init_helpers.ensure_arg_is_subscriptable(subscriptable, 2, "Vector2")
        return cls.__from_values(subscriptable[0], subscriptable[1])

    @classmethod
    def __from_values(cls, x, y):
        return _numpy.array([x, y, 1]).view(cls)

    @classmethod
    def zero(cls):
        return cls(0.0, 0.0)

    @classmethod
    def one(cls):
        return cls(1.0, 1.0)

    @property
    def x(self):
        return self[0]

    @x.setter
    def x(self, value):
        self[0] = value

    @property
    def y(self):
        return self[1]

    @y.setter
    def y(self, value):
        self[1] = value

    def __str__(self):
        return f"[{self.x}, {self.y}]"
