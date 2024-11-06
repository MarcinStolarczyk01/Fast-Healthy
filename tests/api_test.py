from pathlib import Path

import pytest
from starlette.testclient import TestClient

from src.api import app
from src.files_io_manager.files_io_manager import FilesIOManager


client = TestClient(app)

@pytest.mark.parametrize('recipe_body, expected_code', [({
    "name": "meal one",
    "procedure": [
        "Make something",
        "Make something else"
    ],
    "products": {
        "egg": 3.0,
        "butter": 10.0
    }
}, 201)])
def test_post_recipes_should_return_status_code_correct_code(recipe_body: dict, expected_code: int):
    FilesIOManager.RECIPES_PATH = Path(__file__).parent.joinpath('test_files', 'recipes4.json')
    response = client.post('/recipes', json=recipe_body)
    assert expected_code == response.status_code
