from pathlib import Path
import json
from typing import Optional, Iterable
from pydantic import BaseModel, Field

from src.models.recipe.recipe import RecipeModel


class RecipesJsonModel(BaseModel):
    recipes: list[Optional[RecipeModel]] = Field(default=[])


class FilesIOManager:
    RECIPES_PATH = Path(__file__).parent.joinpath("recipes.json")

    @classmethod
    def add_recipe(cls, recipe_json: RecipeModel):
        cls.ensure_recipes_file()

        with open(cls.RECIPES_PATH, mode="r+") as fp:
            file_content = fp.read()

            if file_content:
                json_content = json.loads(file_content)
                recipes = RecipesJsonModel(**json_content)
            else:
                recipes = RecipesJsonModel()

            recipes.recipes.append(recipe_json)
            fp.truncate(0)
            fp.seek(0)
            fp.write(recipes.model_dump_json())

    @classmethod
    def get_recipes(cls) -> RecipesJsonModel:
        cls.ensure_recipes_file()

        with open(cls.RECIPES_PATH, mode="r") as fp:
            recipes = RecipesJsonModel(**json.loads(fp.read()))
        return recipes

    @classmethod
    def drop_recipes(cls, recipes_to_del: Iterable[str]) -> None:
        cls.ensure_recipes_file()

        with open(cls.RECIPES_PATH, mode="r+") as fp:
            recipes_content = json.loads(fp.read())
            present_recipes = RecipesJsonModel(**recipes_content)

            if "*" in recipes_to_del:
                recipes_to_save = RecipesJsonModel()
            else:
                recipes_to_save = RecipesJsonModel()
                recipes_to_save.recipes = [
                    recipe
                    for recipe in present_recipes.recipes
                    if recipe.name not in recipes_to_del
                ]

            fp.truncate(0)
            fp.seek(0)

            fp.write(recipes_to_save.model_dump_json())

    @classmethod
    def ensure_recipes_file(cls) -> None:
        if cls.RECIPES_PATH.exists():
            with open(cls.RECIPES_PATH, mode="r") as fp:
                RecipesJsonModel.model_validate_json(fp.read())
        else:
            with open(cls.RECIPES_PATH, mode="w") as fp:
                fp.write(RecipesJsonModel().model_dump_json())
