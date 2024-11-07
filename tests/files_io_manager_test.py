import json
from pathlib import Path
import os

from src.files_io_manager.files_io_manager import FilesIOManager, RecipesJsonModel
from src.models.recipe.recipe import RecipeModel


def test_add_recipe_should_add_recipe_correctly():
    recipe_json = RecipeModel(
        **{
            "name": "omlet",
            "procedure": ["Make something", "Make something else", "Finish"],
            "products": {"egg": 3, "butter": 10},
        }
    )
    recipes_path = Path(__file__).parent.joinpath("test_files", "recipes.json")
    if recipes_path.exists():
        os.remove(recipes_path)
    recipes_path.touch()
    FilesIOManager.RECIPES_PATH = recipes_path

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

    with open(recipes_path) as fp:
        assert json.loads(fp.read()) == expected_recipes_content

    # todo: What happens when there is no structure in the file? Add empty file creating method to FilesIOManager


def test_add_recipe_should_add_multiple_recipes_correctly():
    recipe1_json = RecipeModel(
        **{
            "name": "omlet",
            "procedure": ["Make something", "Make something else", "Finish"],
            "products": {"egg": 3, "butter": 10},
        }
    )
    recipe2_json = RecipeModel(
        **{
            "name": "omlet",
            "procedure": ["Make something", "Make something else", "Finish"],
            "products": {"egg": 3, "butter": 10},
        }
    )
    recipes_path = Path(__file__).parent.joinpath("test_files", "recipes2.json")

    FilesIOManager.RECIPES_PATH = recipes_path
    if recipes_path.exists():
        os.remove(recipes_path)

    FilesIOManager.add_recipe(recipe1_json)
    FilesIOManager.add_recipe(recipe2_json)

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

    with open(recipes_path) as fp:
        assert json.load(fp) == expected_recipes_content


def test_get_recipes_should_return_all_recipes() -> None:
    recipes_path = Path(__file__).parent.joinpath("test_files", "recipes3.json")

    recipes_to_save = {
        "recipes": [
            {
                "name": "toasts",
                "procedure": ["Make something", "Make something else", "Finish"],
                "products": {"bread": 6, "butter": 15, "ham": 20},
            }
        ]
    }

    with open(recipes_path, "w+") as fp:
        fp.write("")
        fp.write(json.dumps(recipes_to_save))
    FilesIOManager.RECIPES_PATH = recipes_path
    result_recipes = FilesIOManager.get_recipes()

    assert result_recipes == RecipesJsonModel(**recipes_to_save)
