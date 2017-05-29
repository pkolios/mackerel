import configparser
import os
from pathlib import Path
from typing import Any, Optional

from click.core import Context


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


def make_config(path: Optional[str] = None,
                ctx: Optional[Context] = None) -> configparser.ConfigParser:
    config = configparser.ConfigParser()
    # Read default config values
    default_cfg_path = Path(os.path.dirname(os.path.realpath(__file__)))
    with open(default_cfg_path / Path('config.ini')) as f:
        config.read_file(f)
    # Read config file
    if path:
        config.read(path)
    # Override config values with command arguments
    for key in ctx.obj:
        config['mackerel'][key] = str(ctx.obj[key])
    return config
