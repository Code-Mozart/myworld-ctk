import os
import inspect
from typing import Callable, Optional

from src.dir_to_dict.default_callbacks import (
    init_dict_on_begin,
    raise_on_unexpected_file_found,
    raise_on_validation_failed,
    add_file_to_dict_on_after_file_validated,
    return_files_dict_on_finish
)
from src.dir_to_dict.file_system_item import FileSystemItem
from src.dir_to_dict.schema_validator import validate_schema

DIRECTORY = object()
ANY_FILE = object()


def traverse_directory(
        dir_path: str,
        schema: dict | None = None,
        on_begin: Optional[Callable] = init_dict_on_begin,
        on_before_file_validated: Optional[Callable] = None,
        on_unexpected_file_found: Optional[Callable] = raise_on_unexpected_file_found,
        on_additional_file_found: Optional[Callable] = None,
        on_validation_failed: Optional[Callable] = raise_on_validation_failed,
        on_after_file_validated: Optional[Callable] = add_file_to_dict_on_after_file_validated,
        on_finish: Optional[Callable] = return_files_dict_on_finish,
        on_error: Optional[Callable] = None
):
    """
    Loads a directory recursively, processing each file.
    Takes an (optional) schema to validate the directory structure.

    See the readme for more information on schemas.

    The callbacks are called in the following order:

    - on_begin
    - on_before_file_validated
    - on_additional_file_found / on_unexpected_file_found
    - on_validation_failed
    - on_after_file_validated
    - on_finish

    The on_error callback could be called at any time when an error occurs.

    All callbacks are optional. Callbacks are only called with their demanded arguments. For available parameters,
    see below. "Accumulator" parameters returned by on_begin are passed to the other callbacks as kwargs.

    This function returns the result of the on_finish callback, if it is defined. Otherwise, it returns None.

    :param dir_path:
        The path to the directory to load.
    :param schema:
        The schema to validate the directory structure against. See the readme for more information.
    :param on_begin:
        Called before the directory is loaded. This can be used to set up accumulator values that are passed to
        the other callbacks by returning them as a dict. Available parameters: (dir_path, schema)
    :param on_before_file_validated:
        Called before a file is validated. Available parameters: (dir_path, schema, parent_directories, file_path,
        file_name, file_extension, allowed_file_types, **kwargs)
    :param on_unexpected_file_found:
        Called when a file is found that was not expected according to the schema.
        This callback is mutually exclusive with on_additional_file_found because if the schema defines a "*" wildcard,
        then there are no unexpected files. Available parameters: (dir_path, schema, parent_directories, file_path,
        file_name, file_extension, **kwargs)
    :param on_additional_file_found:
        Called when a file is found that was not explicitly defined by the schema but was allowed because of the
        "*" wildcard. Mutually exclusive with on_unexpected_file_found. Neither callback is called when no schema
        is given. Available parameters: (dir_path, schema, parent_directories, file_path, file_name, file_extension,
        allowed_file_types, **kwargs)
    :param on_validation_failed:
        Called when a file has an invalid extension according to the schema. Available parameters: (dir_path, schema,
        parent_directories, file_path, file_name, file_extension, allowed_file_types, file_or_directory, **kwargs)
    :param on_after_file_validated:
        Called after a file has been validated. Available parameters: (dir_path, schema, parent_directories, file_path,
        file_name, file_extension, allowed_file_types, file_or_directory, **kwargs)
    :param on_finish:
        Called after the whole directory has been traversed. Available parameters: (dir_path, schema, **kwargs)
    :param on_error:
        Called when an error occurs. Available parameters: (dir_path, schema, error, **kwargs)
    """
    validate_schema(schema)
    try:
        callback_variables = _call_callback_with_demanded_args(on_begin, dir_path=dir_path, schema=schema)
        _traverse_dir_recursive(
            dir_path=dir_path,
            schema=schema,
            parent_directories=[],
            on_before_file_validated=on_before_file_validated,
            on_unexpected_file_found=on_unexpected_file_found,
            on_additional_file_found=on_additional_file_found,
            on_validation_failed=on_validation_failed,
            on_after_file_validated=on_after_file_validated,
            callback_variables=callback_variables,
        )
        return _call_callback_with_demanded_args(on_finish, dir_path=dir_path, schema=schema, **callback_variables)
    except Exception as e:
        if on_error is None:
            raise e
        _call_callback_with_demanded_args(on_error, dir_path=dir_path, schema=schema, error=e)


def _traverse_dir_recursive(
        dir_path,
        schema,
        parent_directories,
        on_before_file_validated,
        on_unexpected_file_found,
        on_additional_file_found,
        on_validation_failed,
        on_after_file_validated,
        callback_variables,
):
    for full_file_name in os.listdir(dir_path):
        file_path = os.path.join(dir_path, full_file_name)
        file_name, file_extension = _split_file_name(full_file_name)

        if schema is not None:
            schema_entry = schema.get(file_name, None)
            schema_value = schema_entry or schema.get("*", None)
            allowed_types = _get_allowed_file_types(schema_value)
        else:
            allowed_types = [ANY_FILE, DIRECTORY]

        callback_args = dict(
            dir_path=dir_path,
            schema=schema,
            parent_directories=parent_directories,
            file_path=file_path,
            file_name=file_name,
            file_extension=file_extension,
            **callback_variables
        )

        _call_callback_with_demanded_args(
            on_before_file_validated,
            allowed_file_types=allowed_types,
            **callback_args
        )

        if schema is not None and schema_entry is None:
            if schema_value is None:
                _call_callback_with_demanded_args(
                    on_unexpected_file_found,
                    **callback_args
                )
            else:
                _call_callback_with_demanded_args(
                    on_additional_file_found,
                    allowed_file_types=allowed_types,
                    **callback_args
                )

        def _is_type_allowed(file_type):
            if file_type is DIRECTORY:
                return DIRECTORY in allowed_types
            else:
                return ANY_FILE in allowed_types or file_type in allowed_types

        def _validate(file_type, file_or_directory):
            if not _is_type_allowed(file_type):
                _call_callback_with_demanded_args(
                    on_validation_failed,
                    allowed_file_types=allowed_types,
                    file_or_directory=file_or_directory,
                    ** callback_args
                )

            _call_callback_with_demanded_args(
                on_after_file_validated,
                allowed_file_types=allowed_types,
                file_or_directory=file_or_directory,
                **callback_args
            )

        if os.path.isfile(file_path):
            _validate(file_extension, FileSystemItem.FILE)
        elif os.path.isdir(file_path):
            _validate(DIRECTORY, FileSystemItem.DIRECTORY)
            _traverse_dir_recursive(
                dir_path=file_path,
                schema=schema_value if schema is not None else None,
                parent_directories=parent_directories + [file_name],
                on_before_file_validated=on_before_file_validated,
                on_unexpected_file_found=on_unexpected_file_found,
                on_additional_file_found=on_additional_file_found,
                on_validation_failed=on_validation_failed,
                on_after_file_validated=on_after_file_validated,
                callback_variables=callback_variables,
            )
        else:
            # This should never happen as the items come from the file system
            raise ValueError(f"File {file_path} is neither a file nor a directory")


def _split_file_name(full_file_name):
    parts = full_file_name.split(".")
    return parts[0], "".join(["." + part for part in parts[1:]])


def _get_allowed_file_types(schema_value):
    if schema_value is None:
        return []
    if isinstance(schema_value, dict):
        return [DIRECTORY]
    if isinstance(schema_value, str):
        return _parse_file_type(schema_value)
    if isinstance(schema_value, list):
        return [_parse_file_type(file_type) for file_type in schema_value]
    raise ValueError(f"Invalid schema value {schema_value}")


def _parse_file_type(file_type):
    if file_type == "*":
        return DIRECTORY
    elif file_type == ".*":
        return ANY_FILE
    else:
        return file_type


def _call_callback_with_demanded_args(callback, **kwargs):
    if callback is None:
        return

    signature = inspect.signature(callback)
    kwargs_param = next((p for p in signature.parameters.values() if p.kind == inspect.Parameter.VAR_KEYWORD), None)
    if kwargs_param is not None:
        callback_args = kwargs
    else:
        callback_args = {
            k: v for k, v in kwargs.items()
            if k in signature.parameters and signature.parameters[k].kind in [
                inspect.Parameter.KEYWORD_ONLY,
                inspect.Parameter.POSITIONAL_OR_KEYWORD
            ]
        }
    return callback(**callback_args)
