from enum import Enum

from src import dir_to_dict
from src.dir_to_dict.default_callbacks import (
    raise_on_unexpected_file_found,
    add_file_to_dict_on_after_file_validated
)


class __FilesImpl:
    @classmethod
    def raise_on_additional_file_found(cls, file_name, directory_path):
        import os
        raise ValueError(f"Unexpected file {file_name} found in {os.path.abspath(directory_path)}.")

    @classmethod
    def load_yaml(cls, path):
        import yaml

        with open(path, "r") as file:
            return yaml.safe_load(file)

    @classmethod
    def load_file_structure(cls, dir_path, schema, on_unexpected_file_found=None):
        return dir_to_dict.traverse(
            dir_path=dir_path,
            schema=schema,
            on_unexpected_file_found=on_unexpected_file_found or raise_on_unexpected_file_found,
            on_after_file_validated=cls._on_after_file_validated
        )

    @classmethod
    def _on_after_file_validated(cls, **kwargs):
        add_file_to_dict_on_after_file_validated(
            on_before_file_added=cls._load_and_add_file,
            **kwargs
        )

    @classmethod
    def _load_and_add_file(cls, file_path, file_name, file_extension, **kwargs):
        if file_extension in [".yml", ".yaml", ".json"]:
            content = cls.load_yaml(file_path)
        else:
            raise Exception(f"{file_extension} files are not supported")
        return file_name, content


Files = __FilesImpl()


class FileType(Enum):
    DIRECTORY = "directory"
    """A directory."""

    YAML = "yaml"
    """A YAML-like file, i.e. YAML or JSON. The file extension must be .yml, .yaml or .json."""
