"""SARA file module."""

import json
from pathlib import Path
from sara.core.config import sara_files_path
from sara.core.utils import create_path


create_path(sara_files_path)


def save_data_file(name, data):
    """Save followers data to file."""
    storage_path = name
    if not isinstance(name, Path):
        storage_path = Path(name)
    with open(storage_path, 'a+', encoding='utf-8') as files:
        json.dump(data, files, ensure_ascii=False)
        files.write("\n")


def load_data(name):
    """Load data from storage_path and return a list."""
    user_data = []
    storage_path = Path(f'{sara_files_path}/{name}')
    with open(storage_path, "r") as file:
        for line in file:
            try:
                user_data.append(json.loads(line))
            except FileNotFoundError:
                pass
    return user_data
