def exactly_one_of(**kwargs):
    given_args = [{opt: value} for opt, value in kwargs.items() if is_given(value)]

    if len(given_args) == 0:
        option_names = ", ".join(kwargs.keys())
        raise ValueError(f"Expected exactly one of the following options: {option_names}")
    if len(given_args) > 1:
        given_args_names = ", ".join([list(args.keys())[0] for args in given_args])
        raise ValueError(f"The parameters {given_args_names} are mutually exclusive.")

    return list(given_args[0].values())[0]


def maybe(func, *args):
    if not is_given(func):
        return func

    for arg in args:
        if not is_given(arg):
            return arg

    return func(*args)


def is_given(value):
    return value is not None and value is not ...
