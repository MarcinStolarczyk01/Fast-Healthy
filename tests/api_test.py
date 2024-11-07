import json
from http import HTTPStatus
from pathlib import Path

import pytest
from starlette.testclient import TestClient

from api import dietitian
from src.api import app
from src.files_io_manager.files_io_manager import FilesIOManager

client = TestClient(app)


@pytest.mark.parametrize(
    "recipe_body, expected_code",
    [
        (
                {
                    "name": "meal one",
                    "procedure": ["Make something", "Make something else"],
                    "products": {"egg": 3.0, "butter": 10.0},
                },
                HTTPStatus.CREATED,
        ),
        (
                {
                    "name": "meal one",
                    "procedure": "Bad type",
                    "products": {"egg": 3.0, "butter": 10.0},
                },
                HTTPStatus.UNPROCESSABLE_ENTITY,
        ),
        (
                {
                    "name": "meal one",
                    "procedure": [
                        "Brush your teeth!",
                    ],
                    "products": {"egg": 3.0, "butter": 10.0},
                },
                HTTPStatus.INTERNAL_SERVER_ERROR,
        ),
    ],
)
def test_post_recipes_should_return_status_code_correct_code(
        recipe_body: dict, expected_code: int
):
    FilesIOManager.RECIPES_PATH = Path(__file__).parent.joinpath(
        "test_files", "recipes4.json"
    )
    if expected_code == HTTPStatus.INTERNAL_SERVER_ERROR:
        FilesIOManager.RECIPES_PATH = FilesIOManager.RECIPES_PATH.joinpath(
            "dummy string"
        )
    response = client.post("/recipes", json=recipe_body)
    assert expected_code == response.status_code


@pytest.mark.parametrize('recipes_content', [{
    "name": "meal one",
    "procedure": [
        "Brush your teeth!",
    ],
    "products": {"egg": 3.0, "butter": 10.0},
}, {}
])
def test_get_recipes_should_return_expected_json(recipes_content):
    FilesIOManager.RECIPES_PATH = Path(__file__).parent.joinpath('test_files', 'recipes5.json')

    assert dietitian.get_recipes().model_dump_json() == str(recipes_content)