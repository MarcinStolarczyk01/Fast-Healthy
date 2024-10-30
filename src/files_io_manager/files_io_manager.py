from pathlib import Path
import json

from pydantic import BaseModel

from models.recipe.recipe import RecipeModel


class RecipesJsonModel(BaseModel):
    recipes: list[RecipeModel]


class FilesIOManager:
    RECIPES_PATH = Path(__file__).joinpath("recipes.json")

    @classmethod
    def add_recipe(cls, recipe_json: RecipeModel):
        with open(cls.RECIPES_PATH, mode="r+") as fp:
            file_content = fp.read().strip()  # Read existing content

            if file_content:
                json_content = json.loads(file_content)
            else:
                json_content = {}

            recipes = RecipesJsonModel(**json_content)
            recipes.recipes.append(recipe_json)

            fp.seek(0)
            fp.write(recipes.model_dump_json())
            fp.truncate()
