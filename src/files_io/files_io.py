# TODO: files IO toolbox
import json
from pathlib import Path


def open_json(file_path: str | Path) -> dict:
    file_path = Path(file_path)
    if all([file_path.is_file(), file_path.suffix == ".json"]):
        return json.load(open(file_path))
    else:
        raise FileNotFoundError(f"Couldn't find a json file: {file_path}")
