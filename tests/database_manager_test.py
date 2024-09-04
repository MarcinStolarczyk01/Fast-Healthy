from pathlib import Path
import json

from database_manager.database_manager import load_products, load_recipes
from models.product.product import Product
from models.recipe.recipe import Recipe

from models.types.types import ProductsDBType

EXAMPLE_PRODUCTS = {
    "products": [
        {
            "name": "egg",
            "macro": {"fat": 4.8, "protein": 6.3, "carbohydrates": 0.4},
            "unit": "pieces",
        },
        {
            "name": "wholemeal bread",
            "macro": {"fat": 1.7, "protein": 5.9, "carbohydrates": 51.2},
            "unit": "g",
        },
        {
            "name": "butter",
            "macro": {"fat": 81.0, "protein": 0.9, "carbohydrates": 0.1},
            "unit": "g",
        },
    ]
}
EXAMPLE_RECIPES = {
    "recipes": [
        {"name": "breakfast", "products": {"a": 1, "b": 2, "c": 3}},
        {"name": "lunch", "products": {"d": 4, "e": 5, 'f': 6}},
    ]
}

EXAMPLE_PRODUCTS_PATH = Path(__file__).parent.joinpath("test_files", "products.json")
EXAMPLE_RECIPES_PATH = Path(__file__).parent.joinpath("test_files", "recipes.json")


def test_create_database():
    with open(EXAMPLE_PRODUCTS_PATH, mode="w") as fp:
        json.dump(EXAMPLE_PRODUCTS, fp=fp)

    with open(EXAMPLE_RECIPES_PATH, mode="w") as fp:
        json.dump(EXAMPLE_RECIPES, fp=fp)


def test_load_products_should_return_correct_list_of_products():
    products = EXAMPLE_PRODUCTS

    expected_output = [
        Product(name="egg", unit="pieces", fat=4.8, protein=6.3, carbohydrates=0.4),
        Product(name="wholemeal bread", unit="g", fat=1.7, protein=5.9, carbohydrates=51.2),
        Product(name="butter", unit="g", fat=81.0, protein=0.9, carbohydrates=0.1),
    ]

    actual_output = load_products(ProductsDBType(**products))
    assert actual_output == expected_output


def test_load_recipes_should_return_correct_list_of_recipes():
    recipes = EXAMPLE_RECIPES

    expected_output = [
        Recipe(name='breakfast', products={'a': 1, 'b': 2, 'c': 3}, procedure=['Do sth!', 'Do sth else!']),
        Recipe(name="lunch", products={'d': 4, 'e': 5, 'f': 6}, procedure=['Do sth?', 'Do sth else?'])
    ]

    actual_output = load_recipes(**recipes)
    assert actual_output == expected_output
