from pathlib import Path
import yaml

BASE_DIR = str(Path(__file__).resolve().parent.parent)
ConfigPath = BASE_DIR + r"\alpha_calc_config"

pool_size = 16

calc_start = "20180601"
calc_end = "20201231"

universe_options = [
    "HS300", "ZZ500", "ZZ800", "ZZ1000", "ZZ9999"
]


def load_config_yaml(name):
    yaml_file_name = ConfigPath + name
    with open(yaml_file_name, "r") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    return config

