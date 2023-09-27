import os

from src.myworld.io.files import Files

ASSET_ROOT = "res/assets"


class __AssetsImpl:
    _loaded_assets = {}

    def __getattr__(self, key):
        return self._get_or_load_asset(key)

    def _get_or_load_asset(self, key):
        if key not in self._loaded_assets:
            self._load_asset(key)
        return self._loaded_assets[key]

    def _load_asset(self, key):
        # at the moment this reloads all assets
        self._reload_assets()

        if key not in self._loaded_assets:
            raise ValueError(f"Unable to load asset {key}.")
        return self._loaded_assets[key]

    def _reload_assets(self):
        for file in os.listdir(ASSET_ROOT):
            file_path = os.path.join(ASSET_ROOT, file)
            if os.path.isfile(file_path):
                self._load_asset_file(file_path, file)

    def _load_asset_file(self, file, file_name_with_extension):
        file_name, extension = os.path.splitext(file_name_with_extension)
        if extension in [".yaml", ".yml"]:
            content = Files.load_yaml(file)
        else:
            raise ValueError(f"Unable to load asset file {file}. Dont know how to load {extension} files.")
        self._loaded_assets[file_name] = content


Assets = __AssetsImpl()
