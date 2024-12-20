import pathlib
from os.path import abspath, dirname, join
from dynaconf import Dynaconf

setting_dir = dirname(abspath(__file__))

toml_files = list(pathlib.Path(join(setting_dir)).glob('*.toml')) # includes hidden files
settings = Dynaconf(
    envvar_prefix=False,
    merge_enabled=True,
    settings_files=toml_files,
)