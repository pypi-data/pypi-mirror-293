import os
import sys
import toml
from dataclasses import dataclass, is_dataclass, field, fields
from typing import List, Optional, Dict, Any, Type, TypeVar, get_origin, get_args

from pathlib import Path
from xdg import xdg_config_home


def canonical_config_dir() -> Path:
    if sys.platform == "linux":
        return xdg_config_home()
    elif sys.platform == "win32":
        return Path(os.environ["APPDATA"])
    elif sys.platform == "darwin":
        # return Path(os.environ["HOME"]) / "Library" / "Preferences"
        # use .config instead, it makes more sense
        return Path(os.environ["HOME"]) / ".config"


def canonical_config_base(app_name):
    return canonical_config_dir() / app_name


def canonical_config_file(app_name, config_file_name):
    return canonical_config_base(app_name) / config_file_name


class ConfigError(Exception):
    def __init__(self, message=""):
        super().__init__(message)


class TomlConfigFile:
    def get_config_section(self, section, required=False):
        if section not in self.config:
            if required:
                raise ConfigError(f"config file missing [{section}] section")
            else:
                return {}
        return self.config[section]

    def get_config_value(self, table, key, default=None, required=False):
        if key not in table:
            if required:
                raise ConfigError(f"config table {table} missing {key} key")
            else:
                return default
        return table[key]

    def load_from(self, config_path, wizard_callback=None) -> bool:
        # ensure the config file exists
        if not os.path.exists(config_path):
            # show a wizard to create the config file
            if wizard_callback:
                if not wizard_callback(config_path):
                    return False

        with open(config_path, "r") as conf_file:
            self.config = toml.load(conf_file)

        return True


T = TypeVar("T")


def parse_config_model(config_class: Type[T], toml_str: str) -> T:
    toml_data = toml.loads(toml_str)
    return _parse_config_recursive(config_class, toml_data)


def _parse_config_recursive(cls: Type[Any], data: Any) -> Any:
    # print(f"parse_config_recursive: cls={cls}, data={data}")

    # base case: if the class is a simple type, return the data as is
    if cls in (int, float, str, bool) or cls is Any:
        return data

    # if the class is a dataclass, create an instance and fill its fields
    if is_dataclass(cls):
        kwargs = {}
        cls_fields = fields(cls)
        # print(f"cls_fields={cls_fields}")
        for field in cls_fields:
            if field.name in data:
                kwargs[field.name] = _parse_config_recursive(
                    field.type, data[field.name]
                )
            elif field.default is not field.default_factory:
                # use default value if provided and not in data
                kwargs[field.name] = field.default
        return cls(**kwargs)

    # if the class is a list, parse each item in the list
    if get_origin(cls) == list:
        item_type = get_args(cls)[0]
        return [_parse_config_recursive(item_type, item) for item in data]

    # if the class is not a dataclass, it might be a nested class
    # try to initialize it and parse its attributes
    if isinstance(data, dict):
        instance = cls()
        for key, value in data.items():
            if hasattr(cls, key):
                attr = getattr(cls, key)
                if isinstance(attr, type):
                    # if the attribute is a class, use it as the type
                    attr_type = attr
                else:
                    # otherwise, use the type of the attribute
                    attr_type = type(attr)
                setattr(instance, key, _parse_config_recursive(attr_type, value))
        return instance

    # if we can't handle the type, return the data as is
    return data


def config_model_to_dict(obj: Any) -> Dict[str, Any]:
    # if the object is None, return None
    if obj is None:
        return None

    # if the object is a simple type, return it as is
    if isinstance(obj, (int, float, str, bool)):
        return obj

    # if the object is a list, recursively convert each item
    if isinstance(obj, list):
        return [config_model_to_dict(item) for item in obj]

    # if the object is a dataclass, convert it to a dict
    if is_dataclass(obj):
        return {
            field.name: config_model_to_dict(getattr(obj, field.name))
            for field in fields(obj)
        }

    # if the object is a custom class (non-dataclass), convert its __dict__
    if hasattr(obj, "__dict__"):
        return {
            key: config_model_to_dict(value)
            for key, value in obj.__dict__.items()
            if not key.startswith("_")  # exclude private attributes
        }

    # if we can't handle the type, return its string representation
    return str(obj)


def serialize_config_model(config: Any) -> str:
    config_dict = config_model_to_dict(config)
    return toml.dumps(config_dict)


def test_config_serialization(config_class: Type[T], config_file: str):
    """
    Test the serialization and parsing of a config model to ensure compatibility.

    Args:
        config_class: The class of the config model
        config_file: Path to the TOML config file
    """
    # Read the original TOML file
    with open(config_file, "r") as file:
        original_toml = file.read()

    # Parse the original TOML into a config object
    original_config = parse_config_model(config_class, original_toml)

    # Serialize the config object back to TOML
    serialized_toml = serialize_config_model(original_config)

    # Parse the serialized TOML into a new config object
    reparsed_config = parse_config_model(config_class, serialized_toml)

    # Convert both configs to dictionaries for comparison
    original_dict = config_model_to_dict(original_config)
    reparsed_dict = config_model_to_dict(reparsed_config)

    # Compare the dictionaries
    assert (
        original_dict == reparsed_dict
    ), "Serialized and reparsed config doesn't match the original"

    print("Serialization test passed: Original and reparsed configs match.")

    # Optional: Print both TOML strings for manual inspection
    print("\nOriginal TOML:")
    print(original_toml)
    print("\nSerialized TOML:")
    print(serialized_toml)
