from src.dir_to_dict.loader import traverse_directory

if __name__ == '__main__':
    import yaml
    d = traverse_directory(
        dir_path="."
    )
    print(yaml.dump(d))
