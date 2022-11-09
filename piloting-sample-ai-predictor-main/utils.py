import json
import os


def print_env_vars():
    for k, v in os.environ.items():
        print(f'{k}={v}')


def str2bool(value: str):
    return json.loads(value.lower())
