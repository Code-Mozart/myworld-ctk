import re


def validate_schema(schema: dict | None):
    if schema is None:
        return None

    _validate_schema(schema)


def _validate_schema(schema):
    if not isinstance(schema, dict):
        raise ValueError(f"Schema must be a dict, not {type(schema)}")

    for k, v in schema.items():
        if not isinstance(k, str):
            raise ValueError(f"Schema keys must be strings, not {type(k)}")
        _validate_file_name_string(k)

        if isinstance(v, dict):
            _validate_schema(v)
        elif isinstance(v, list):
            _validate_type_list(v)
        elif isinstance(v, str):
            _validate_type_string(v)


def _validate_file_name_string(file_name_string):
    if not file_name_string:
        raise ValueError(f"File/directory names must not be empty strings")

    if not re.match(r"^(.?\w+)|\*$", file_name_string):
        raise ValueError(
            f"File/directory names may only contain alphanumeric characters and underscores or be the "
            f"'*' wildcard, but got '{file_name_string}'"
        )


def _validate_type_list(type_list):
    allow_any_extension = False
    allowed_types_set = set()
    for allowed_type in type_list:
        if not isinstance(allowed_type, str):
            raise ValueError(f"Schema type lists must only contain strings, not {type(allowed_type)}")
        type_class = _validate_type_string(allowed_type)

        if type_class == "extension_wildcard":
            allow_any_extension = True
        elif type_class == "extension" and allow_any_extension:
            raise ValueError(
                f"Schema type lists may not specify allowed extensions if the extension wildcard '*' is present, "
                f"but got '{allowed_type}'"
            )

        if allowed_type in allowed_types_set:
            raise ValueError(
                f"Schema type lists may not contain duplicate entries, but got '{allowed_type}' twice"
            )
        allowed_types_set.add(allowed_type)


def _validate_type_string(type_string):
    if re.match(r"^\.\*$", type_string):
        return "extension_wildcard"
    if re.match(r"^\*$", type_string):
        return "directory"
    elif re.match(r"^\.[a-zA-Z]+$", type_string):
        return "extension"
    elif re.match(r"regex=\(.+\)", type_string):
        _validate_regex(type_string[6:])
    else:
        raise ValueError(
            f"Schema types must be file extensions, the directory wildcard '*' or the file wildcard '.*', "
            f"but got '{type_string}'"
        )


def _validate_regex(regex):
    try:
        re.compile(regex)
    except re.error as e:
        raise ValueError(f"Invalid regex ({regex})") from e
