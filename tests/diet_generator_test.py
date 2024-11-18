import json
import time
from pathlib import Path

from src.models.recipe.recipe import Recipe, RecipeModel
from src.files_io_manager.files_io_manager import FilesIOManager


def test_placeholder():
    recipes_json_path = Path(__file__).parent.joinpath('test_files', 'sample_recipes','generated_recipes.json')
    recipes_content = json.load(open(recipes_json_path))['recipes']

    start = time.time()
    FilesIOManager.RECIPES_PATH = recipes_json_path.parents[1].joinpath('saved_recipes.json')

    recipes = []
    for recipe in recipes_content[:15]:
        recipes.append(Recipe(RecipeModel(**recipe)))

    print(f"\n\nExecution time: {time.time() - start:.4f} seconds")

    from src.dietitian.diet_generator.diet_generator import DietScheduler
    diet_generator = DietScheduler(recipes=tuple(recipes),
                                   kcal_goal=3000,
                                   meals_number=4)

    _ = diet_generator.schedule()
