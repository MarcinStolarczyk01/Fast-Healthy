import json
import time
from pathlib import Path

import pytest

from src.models.recipe.recipe import Recipe, RecipeModel
from src.files_io_manager.files_io_manager import FilesIOManager

# integration test
pytest.mark.parametrize(
    "sample_recipes_path",
    [
        Path(__file__).parent.joinpath(
            "test_files", "sample_recipes", "generated_recipes.json"
        )
    ],
)


def test_placeholder(sample_recipes_path, tmp_path: Path) -> None:
    recipes_content = json.load(open(sample_recipes_path))["recipes"]

    start = time.time()
    FilesIOManager.RECIPES_PATH = sample_recipes_path.parents[1].joinpath(
        "saved_recipes.json"
    )

    recipes = []
    for recipe in recipes_content[:15]:
        recipes.append(Recipe(RecipeModel(**recipe)))

    print(f"\n\nExecution time: {time.time() - start} seconds")

    from src.dietitian.diet_generator.diet_generator import DietScheduler

    diet_generator = DietScheduler(
        recipes=tuple(recipes), kcal_goal=3000, meals_number=4
    )

    _ = diet_generator.schedule()
