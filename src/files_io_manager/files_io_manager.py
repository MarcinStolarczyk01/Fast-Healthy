from pathlib import Path
import json
from typing import Optional

from pydantic import BaseModel, Field

from src.models.recipe.recipe import RecipeModel


class RecipesJsonModel(BaseModel):
    recipes: list[Optional[RecipeModel]] = Field(default=[])


class FilesIOManager:
    RECIPES_PATH = Path(__file__).joinpath("recipes.json")

    @classmethod
    def add_recipe(cls, recipe_json: RecipeModel):
        cls.RECIPES_PATH.touch()
        with open(cls.RECIPES_PATH, mode="r+") as fp:
            file_content = fp.read()

            if file_content:
                json_content = json.loads(file_content)
                recipes = RecipesJsonModel(**json_content)
            else:
                recipes = RecipesJsonModel()

            recipes.recipes.append(recipe_json)
            fp.seek(0)
            fp.write(recipes.model_dump_json())

    @classmethod
    def get_recipes(cls) -> RecipesJsonModel:
        if not cls.RECIPES_PATH.exists():
            with cls.RECIPES_PATH.open(mode='w+') as fp:
                fp.write('{}')
        with open(cls.RECIPES_PATH, mode="r") as fp:
            recipes = RecipesJsonModel(**json.loads(fp.read()))
        return recipes
