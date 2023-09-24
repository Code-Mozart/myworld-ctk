from pygame import Color


def as_hex(color: Color) -> str:
    return f"#{color.r:02x}{color.g:02x}{color.b:02x}"
