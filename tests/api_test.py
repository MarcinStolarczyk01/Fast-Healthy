import json
import os
from http import HTTPStatus
from pathlib import Path

import pytest
from starlette.testclient import TestClient

from src.api import app
from src.files_io_manager.files_io_manager import FilesIOManager
from threading import Lock

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


@pytest.mark.parametrize(
    "recipes_content",
    [
        {
            "recipes": [
                {
                    "name": "meal one",
                    "procedure": [
                        "Brush your teeth!",
                    ],
                    "products": {"egg": 3.0, "butter": 10.0},
                }
            ]
        },
        {"recipes": []},
    ],
)
def test_get_recipes_should_return_expected_json(recipes_content):
    recipes_path = Path(__file__).parent.joinpath("test_files", "recipes5.json")
    FilesIOManager.RECIPES_PATH = recipes_path

    with open(recipes_path, "w+") as fp:
        fp.write(json.dumps(recipes_content))

    response = client.get("/recipes")

    assert json.loads(response.json()) == recipes_content


@pytest.mark.parametrize(
    "recipes_to_del, result_recipes_content, fnum",
    [
        ({"recipes": ["*"]}, {"recipes": []}, 6),
        (
                {"recipes": ["pancakes", "hamburger"]},
                {
                    "recipes": [
                        {
                            "name": "omlet",
                            "procedure": [
                                "Make something",
                                "Make something else",
                                "Finish",
                            ],
                            "products": {"egg": 3.0, "butter": 10.0},
                        }
                    ]
                },
        7),
    ],
)
def test_post_recipes_delete_removes_specified_recipes(
        recipes_to_del, result_recipes_content, fnum
):
    FilesIOManager.RECIPES_PATH = Path(__file__).parent.joinpath('test_files', f'recipes{fnum}.json')

    # Write initial recipes to the file
    recipes_content = {
        "recipes": [
            {
                "name": "omlet",
                "procedure": ["Make something", "Make something else", "Finish"],
                "products": {"egg": 3.0, "butter": 10.0},
            },
            {
                "name": "pancakes",
                "procedure": ["Make something", "Make something else", "Finish"],
                "products": {"egg": 3.0, "flour": 100, "oil": 10},
            },
            {
                "name": "hamburger",
                "procedure": ["Make something", "Make something else", "Finish"],
                "products": {"beef": 150.0, "bread": 100, "oil": 10, "salad": 30},
            },
        ]
    }
    with open(FilesIOManager.RECIPES_PATH, "w") as fp:
        json.dump(recipes_content, fp)

    # Call the API to delete recipes
    response = client.post("/recipes/delete", json=recipes_to_del)

    assert json.loads(response.json()) == {"message": "Successfully deleted recipes"}

    # Read back the content to verify deletion
    with open(FilesIOManager.RECIPES_PATH, "r") as fp:
        assert json.load(fp) == result_recipes_content
