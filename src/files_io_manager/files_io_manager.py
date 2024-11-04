from pathlib import Path
import json
from typing import Optional

from pydantic import BaseModel, Field

from models.recipe.recipe import RecipeModel


class RecipesJsonModel(BaseModel):
    recipes: list[Optional[RecipeModel]] = Field(default=[])


class FilesIOManager:
    RECIPES_PATH = Path(__file__).joinpath("recipes.json")

    @classmethod
    def add_recipe(cls, recipe_json: RecipeModel):
        with open(cls.RECIPES_PATH, mode="w+") as fp:
            file_content = fp.read()

            if file_content:
                json_content = json.loads(file_content)
                recipes = RecipesJsonModel(**json_content)
            else:
                recipes = RecipesJsonModel()

            recipes.recipes.append(recipe_json)
            fp.write(recipes.model_dump_json())
