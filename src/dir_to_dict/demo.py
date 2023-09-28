from src.dir_to_dict.loader import traverse_directory

if __name__ == '__main__':
    import yaml
    d = traverse_directory(
        dir_path="/Users/markusmarewitz/dev/myworld-py/res",
        schema={
            "assets": {
                "world_materials": ".yml",
                "project_templates": {
                    "*": {
                        "project": ".yml",
                        "worlds": {
                            "*": ".yml"
                        }
                    }
                }
            },
            "locales": {
                "*": "regex=(^\\.\\w{2}\\.yml$)"
            }
        }
    )
    print(yaml.dump(d))
