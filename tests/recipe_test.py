from pydantic import ValidationError

from src.models.recipe.recipe import Recipe
import pytest


@pytest.mark.parametrize(
    "recipe_section",
    [
        {
            "name": "omlet",
            "procedure": ["Make something", "Make something else", "Finish"],
            "products": {"egg": 3, "butter": 10},
        }
    ],
)
def test_recipe_should_create_object_from_dict(recipe_section):

    recipe = Recipe(recipe_section)

    assert recipe.name == "omlet"
    assert recipe.procedure == ("Make something", "Make something else", "Finish")
    assert len(recipe.products) == 2


@pytest.mark.parametrize(
    "recipe_section, error_type",
    [
        (
            {
                "recipe title": "omlet",
                "procedure": ["Make something", "Make something else", "Finish"],
                "products": {"egg": 3, "butter": 10},
            },
            ValidationError,
        ),
    ],
)
def test_recipe_should_raise_error(recipe_section, error_type):
    with pytest.raises(error_type):
        Recipe(recipe_section)
