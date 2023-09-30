def ensure_arg_is_subscriptable(arg, len_, name):
    if not hasattr(arg, "__len__"):
        raise ValueError(f"When initializing {name} with only one argument, it must have a length")
    if len(arg) != len_:
        raise ValueError(f"When initializing {name} with a subscriptable, it must have exactly {len_} elements, "
                         f"but {len(arg)} where given")
    if not hasattr(arg, "__getitem__"):
        raise ValueError(f"When initializing {name} with only one argument, it must be subscriptable")
