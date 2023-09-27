from enum import Enum


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
    def load_file_structure(cls, file_path, structure, on_additional_file_found):
        import os

        cls._validate_file_structure_arg(structure)

        files = {}

        def __handle_file():
            name_without_extension, extension = os.path.splitext(current_file_name)
            expected_file_type = structure.get(name_without_extension, None)
            if expected_file_type is None:
                on_additional_file_found(current_file_name, file_path)
            cls._validate_file_type(expected_file_type, extension, path=current_file_path)

            files[name_without_extension] = cls._load_file(file_path=current_file_path, file_type=expected_file_type)

        def __handle_directory():
            expected_file_type = structure.get(current_file_name, None)
            if expected_file_type is None:
                on_additional_file_found(current_file_name, file_path)
            cls._validate_file_type(expected_file_type, path=current_file_path)

            files[current_file_name] = cls.load_file_structure(
                file_path=current_file_path,
                structure=structure[current_file_name],
                on_additional_file_found=on_additional_file_found
            )

        for current_file_name in os.listdir(file_path):
            current_file_path = os.path.join(file_path, current_file_name)
            if os.path.isfile(current_file_path):
                __handle_file()
            elif os.path.isdir(current_file_path):
                __handle_directory()


Files = __FilesImpl()


class FileType(Enum):
    DIRECTORY = "directory"
    """A directory."""

    YAML = "yaml"
    """A YAML-like file, i.e. YAML or JSON. The file extension must be .yml, .yaml or .json."""
