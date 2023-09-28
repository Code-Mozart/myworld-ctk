from typing import Callable, Optional

from src.dir_to_dict.file_system_item import FileSystemItem


def init_dict_on_begin():
    return {"files": {}}


def raise_on_unexpected_file_found(dir_path, schema, file_name):
    import os
    raise ValueError(
        f"Unexpected file {file_name} found in {os.path.abspath(dir_path)}. "
        f"Only these files are allowed: {schema.keys()}"
    )


def raise_on_validation_failed(dir_path, file_name, file_extension, allowed_file_types):
    import os
    raise ValueError(
        f"File {file_name} in {os.path.abspath(dir_path)} has an invalid extension {file_extension}. "
        f"Only these extensions are allowed: {allowed_file_types}"
    )


def add_file_to_dict_on_after_file_validated(
        parent_directories,
        file_path,
        file_name,
        file_extension,
        file_or_directory,
        on_before_file_added: Optional[Callable] = None,
        on_after_file_added: Optional[Callable] = None,
        **kwargs
):
    """
    Default callback that adds the file to the constructed file dictionary. This callback itself supports two
    optional callbacks.

    :param on_before_file_added:
        Called before adding the file to the dictionary. Must take these arguments: file_path, file_name,
        file_extension. The callback must return a tuple (key, value) that is added to the dictionary instead.
    :param on_after_file_added:
        Called after the file was added (perhaps with the overriden value from the other callback).
        Must take these arguments: file_path, file_name, file_extension, files_dictionary, parent_directories,
        added_value. The return value of this callback is ignored.
    """

    if file_or_directory is not FileSystemItem.FILE:
        return

    files = kwargs["files"]
    current_dict = files
    for directory in parent_directories:
        if directory not in current_dict:
            current_dict[directory] = {}
        current_dict = current_dict[directory]

    if on_before_file_added is None:
        key = f"{file_name}{file_extension}"
        value = f"{file_extension} file"
        if file_extension.startswith("."):
            value = value[1:]
    else:
        key, value = on_before_file_added(file_path=file_path, file_name=file_name, file_extension=file_extension)
    current_dict[key] = value
    if on_after_file_added is not None:
        on_after_file_added(
            file_path=file_path,
            file_name=file_name,
            file_extension=file_extension,
            files_dictionary=files,
            parent_directories=parent_directories,
            added_value=value,
        )


def return_files_dict_on_finish(**kwargs):
    return kwargs["files"]
