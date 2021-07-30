"""
Generate saraBotTagger metadata
"""
import sys
import json

from sara.core.metadados import get_user_metadata
import pandas as pd
from pathlib import Path


def load_data(name):
    """Load data."""
    user_data = []
    with open(name, "r") as file:
        for line in file:
            try:
                user_data.append(json.loads(line))
            except FileNotFoundError:
                pass
    return user_data


def get_inputed_data():
    """Handler to get the inputed data using arguments."""
    try:
        path_to_data = sys.argv[1]
    except IndexError as error_msg:
        print(f"Error {error_msg}")
        print("Please input the data to be loaded.")
        sys.exit(-1)
    return Path(path_to_data)


def main(path_to_data):
    """main method."""
    loaded_data = []
    users = {}
    for item in path_to_data.iterdir():
        if item.is_file() and item.suffix == '.txt':
            data = load_data(item)
            loaded_data.append(data)

    for user in loaded_data:

        metadata = get_user_metadata(user.pop(), '2021-05-21')
        users[metadata['id_str']] = metadata
    table = pd.DataFrame(list(users.values()))
    table.to_csv('astro_metadata.csv', index=False)


if __name__ == "__main__":
    path_to_data = get_inputed_data()
    main(path_to_data)
