import numpy as _numpy

from src.myworld.math2d import init_helpers


class Transform2(_numpy.ndarray):
    def __new__(cls, *args, translation=..., rotation=..., scale=...):
        if len(args) == 0:
            if any(arg is not ... for arg in (translation, rotation, scale)):
                if translation is ...:
                    translation = [0.0, 0.0],
                if rotation is ...:
                    rotation = 0.0
                if scale is ...:
                    scale = [1.0, 1.0]
                return cls.__from_elements(translation, rotation, scale)
            else:
                return cls.identity()

        if any(arg is not ... for arg in (translation, rotation, scale)):
            raise ValueError(
                "When initializing Transform2 with positional arguments, no keyword arguments must be specified"
            )

        if len(args) == 1:
            return cls.__from_subscriptable(args[0])
        if len(args) == 3:
            return cls.__from_elements(args[0], args[1], args[2])

        raise ValueError(
            "Transform2 must be initialized with either no arguments, a subscriptable,"
            "or translation, rotation, and scale as positional arguments or keyword arguments"
        )

    @classmethod
    def __from_subscriptable(cls, subscriptable):
        init_helpers.ensure_arg_is_subscriptable(subscriptable, 3, "Transform2")
        return cls.__from_elements(subscriptable[0], subscriptable[1], subscriptable[2])

    @classmethod
    def __from_elements(cls, translation, rotation, scale):
        t = cls.translation(translation)
        r = cls.rotation(rotation)
        s = cls.scale(scale)
        return t @ r @ s

    @classmethod
    def identity(cls):
        return _numpy.identity(3).view(cls)

    @classmethod
    def __parse_args(cls, args, x, y, method_name):
        if len(args) == 0:
            if x is ... or y is ...:
                raise ValueError(
                    f"When initializing Transform2.{method_name} with no positional arguments,"
                    f"both x and y must be specified"
                )
            return [x, y]
        if x is not ... or y is not ...:
            raise ValueError(
                f"When initializing Transform2.{method_name} with positional arguments,"
                f"no keyword arguments must be specified"
            )
        if len(args) == 1:
            arg = args[0]
            init_helpers.ensure_arg_is_subscriptable(arg, 2, f"Vector2.{method_name}")
        if len(args) == 2:
            return args

        raise ValueError(
            f"Transform2.{method_name} must be initialized with either no arguments, a subscriptable,"
            f"or x and y as positional arguments or keyword arguments"
        )

    @classmethod
    def parse_single_arg(cls, args, arg, arg_name, method_name):
        if len(args) == 0:
            if arg is ...:
                raise ValueError(
                    f"When initializing Transform2.{method_name} with no positional arguments,"
                    f"{arg_name} must be specified"
                )
            return arg
        if arg is not ...:
            raise ValueError(
                f"When initializing Transform2.{method_name} with positional arguments,"
                f"no keyword arguments must be specified"
            )
        if len(args) == 1:
            return args[0]

        raise ValueError(
            f"Transform2.{method_name} must be initialized {arg_name} as either a positional argument,"
            f"or a keyword argument"
        )

    @classmethod
    def translation(cls, *args, x=..., y=...):
        values = cls.__parse_args(args, x, y, method_name="translation")

        inst = cls.identity()
        inst[0:2, 2] = values
        return inst

    @classmethod
    def rotation(cls, *args, angle=...):
        angle = cls.parse_single_arg(args, angle, "angle", method_name="rotation")

        cos = _numpy.cos(angle)
        sin = _numpy.sin(angle)

        inst = cls.identity()
        inst[0:2, 0:2] = [[cos, -sin], [sin, cos]]
        return inst

    @classmethod
    def scale(cls, *args, x=..., y=...):
        values = cls.__parse_args(args, x, y, method_name="scale")

        inst = cls.identity()
        inst[0, 0] = values[0]
        inst[1, 1] = values[1]
        return inst

    def multiply(self, vector: "Vector2"):
        return (self @ vector).view(vector.__class__)

    def inverse(self):
        return _numpy.linalg.inv(self).view(Transform2)
