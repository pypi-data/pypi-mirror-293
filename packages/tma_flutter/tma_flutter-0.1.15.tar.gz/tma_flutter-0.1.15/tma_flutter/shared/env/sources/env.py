import yaml
from enum import Enum
from pathlib import Path
from typing import Optional


current_dir = Path(__file__).absolute().parent
file_name = "env.yaml"
env_file_path = current_dir.joinpath(file_name)


class ENV_KEY(str, Enum):
    prefix = "prefix"


def write_yaml(env_dict: dict):
    with open(env_file_path, "w") as f:
        yaml.dump(env_dict, f)
    return


def read_yaml() -> Optional[dict]:
    try:
        with open(env_file_path, "r") as f:
            yaml_file = yaml.safe_load(f)
        return yaml_file
    except:
        return None


def get_value(key: ENV_KEY) -> Optional[str]:
    env_dict = read_yaml()
    return env_dict.get(key) if env_dict != None else None
