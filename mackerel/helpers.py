import configparser
import os
from pathlib import Path
from typing import Any


class cached_property:
    def __init__(self, func: Any) -> None:
        self.__doc__ = getattr(func, '__doc__')
        self.func = func

    def __get__(self, obj: Any, cls: Any) -> Any:
        if obj is None:
            return self
        value = obj.__dict__[self.func.__name__] = self.func(obj)
        return value


def touch(path: Path) -> bool:
    if not path.parent.exists():
        path.parent.mkdir(parents=True)
    path.touch()
    return True


def make_config(site_path: Path) -> configparser.ConfigParser:
    config = configparser.ConfigParser()
    # Read default config values
    default_cfg_path = Path(os.path.dirname(os.path.realpath(__file__)))
    with open(default_cfg_path / Path('config.ini')) as f:
        config.read_file(f)
    # Read config file
    config.read(str(Path(site_path) / Path('.mackerelconfig')))
    return config
