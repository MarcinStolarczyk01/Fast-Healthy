import json
from pathlib import Path

import pytest

from src.files_io_manager.files_io_manager import FilesIOManager, RecipesJsonModel
from src.models.recipe.recipe import RecipeModel


@pytest.mark.parametrize(
    "recipe",
    [
        {
            "name": "omlet",
            "procedure": ["Make something", "Make something else", "Finish"],
            "products": {"egg": 3, "butter": 10},
        }
    ],
)
def test_add_recipe_should_add_recipe_correctly(recipe, tmp_path: Path):
    recipe_json = RecipeModel(**recipe)
    FilesIOManager.RECIPES_PATH = tmp_path.joinpath("recipes.json")

    FilesIOManager.add_recipe(recipe_json)

    expected_recipes_content = {
        "recipes": [
            {
                "name": "omlet",
                "procedure": ["Make something", "Make something else", "Finish"],
                "products": {"egg": 3, "butter": 10},
            }
        ]
    }

    with open(FilesIOManager.RECIPES_PATH) as fp:
        assert json.loads(fp.read()) == expected_recipes_content

    # todo: What happens when there is no structure in the file? Add empty file creating method to FilesIOManager


@pytest.mark.parametrize(
    "recipe1, recipe2",
    [
        (
            {
                "name": "omlet",
                "procedure": ["Make something", "Make something else", "Finish"],
                "products": {"egg": 3, "butter": 10},
            },
            {
                "name": "omlet",
                "procedure": ["Make something", "Make something else", "Finish"],
                "products": {"egg": 3, "butter": 10},
            },
        )
    ],
)
def test_add_recipe_should_add_multiple_recipes_correctly(
    recipe1, recipe2, tmp_path: Path
):
    FilesIOManager.RECIPES_PATH = tmp_path.joinpath("recipes.json")
    FilesIOManager.add_recipe(RecipeModel(**recipe1))
    FilesIOManager.add_recipe(RecipeModel(**recipe2))

    expected_recipes_content = {
        "recipes": [
            {
                "name": "omlet",
                "procedure": ["Make something", "Make something else", "Finish"],
                "products": {"egg": 3, "butter": 10},
            },
            {
                "name": "omlet",
                "procedure": ["Make something", "Make something else", "Finish"],
                "products": {"egg": 3, "butter": 10},
            },
        ]
    }

    with open(FilesIOManager.RECIPES_PATH) as fp:
        assert json.load(fp) == expected_recipes_content


@pytest.mark.parametrize(
    "recipes_to_save",
    [
        {
            "recipes": [
                {
                    "name": "toasts",
                    "procedure": ["Make something", "Make something else", "Finish"],
                    "products": {"bread": 6, "butter": 15, "ham": 20},
                }
            ]
        }
    ],
)
def test_get_recipes_should_return_all_recipes(recipes_to_save, tmp_path: Path) -> None:
    FilesIOManager.RECIPES_PATH = tmp_path.joinpath("recipes.json")

    with open(FilesIOManager.RECIPES_PATH, "w") as fp:
        fp.write(json.dumps(recipes_to_save))
    result_recipes = FilesIOManager.get_recipes()

    assert result_recipes == RecipesJsonModel(**recipes_to_save)
