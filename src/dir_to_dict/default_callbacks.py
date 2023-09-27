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
        parent_directories, file_name, file_extension, file_or_directory, **kwargs
):

    if file_or_directory is not FileSystemItem.FILE:
        return

    files = kwargs["files"]
    current_dict = files
    for directory in parent_directories:
        if directory not in current_dict:
            current_dict[directory] = {}
        current_dict = current_dict[directory]

    value = f"{file_extension} file"
    if file_extension.startswith("."):
        value = value[1:]
    current_dict[f"{file_name}{file_extension}"] = value


def return_files_dict_on_finish(**kwargs):
    return kwargs["files"]
