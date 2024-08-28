from files_io.files_io import open_json
import pytest
from pathlib import Path
import json


def test_open_json_should_raise_FileNotFoundError():
    not_existing_path = "this/is/random/path"
    with pytest.raises(
        FileNotFoundError, match="Couldn't find a json file: " + not_existing_path
    ):
        open_json(not_existing_path)


def test_open_json_should_return_valid_dict():
    content = {
        "recipes": [
            {"name": "meal1", "products": {"prod1": 10, "prod2": None}},
            {"name": "meal2", "products": {"prod3": 25, "prod4": 150}},
        ]
    }
    # Create a test file
    file_path = Path(__file__).parent.joinpath("test_files", "recipes.json")
    file_path.parent.mkdir(exist_ok=True)
    json.dump(content, fp=open(file_path, mode="w"))

    # Assertion
    assert open_json(file_path) == content
