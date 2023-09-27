# dir_to_dict

This is a python module for working with directory structures. It recursively traverses a directory
and touches all files and directories. By default, it just constructs a dictionary representation
of the directory, but this behaviour can be customized via callbacks.

dir_to_dict also supports validating the directory structure against a schema.


## Schema

The schema is a dictionary that describes the structure of the directory.

For example:
```python
{
    "my_file_name": ".yml",
    "my_dir": {
        "file_in_dir": [".txt", ".html", ".md"],
        "subdir": {
            "*": [".json", ".yml", ".yaml"]
        }
    },
    "*": ".*"
}
```

This is an example for a valid directory structure for this schema:
```
├ my_dir/
│ ├ file_in_dir.txt
│ └ subdir/
│   ├ file_1.json
│   ├ file_2.json
│   ├ file_3.yml
│   ├ file_4.yaml
│   └ file_5.json
├ my_file_name.yml
└ additional_file.exe
```

As you can see, the schema is a recursive dictionary. The keys are the names of the
files/directories and the values are the expected file extension(s) or a nested schema.

The `*` key is a wildcard allowing any file name and any number of files.

The `.*` value is a wildcard allowing any file. `*` allows any directory. To allow both
directories and files, use `"*": [".*", "*"]`.
