from pathlib import Path
import json

from database_manager.database_manager import load_products
from models.product.product import Product

EXAMPLE_PRODUCTS = {
    "products": [
        {
            "name": "egg",
            "macro": {
                "fat": 4.8,
                "protein": 6.3,
                "carbohydrates": 0.4
            },
            "unit": "pieces"
        },
        {
            "name": "wholemeal bread",
            "macro": {
                "fat": 1.7,
                "protein": 5.9,
                "carbohydrates": 51.2
            },
            "unit": "g"
        },
        {
            "name": "butter",
            "macro": {
                "fat": 81,
                "protein": 0.9,
                "carbohydrates": 0.1
            },
            "unit": "g"
        }
    ]
}
EXAMPLE_RECIPES = {
    "recipes": [
        {
            "name": "meal1",
            "products": {
                "prod1": 10,
                "prod2": None
            }
        },
        {
            "name": "meal2",
            "products": {
                "prod3": 25,
                "prod4": 150
            }
        }
    ]
}


EXAMPLE_PRODUCTS_PATH = Path(__file__).parent.joinpath("test_files", "products.json")
EXAMPLE_RECIPES_PATH = Path(__file__).parent.joinpath("test_files", "recipes.json")


def create_test_database():
    with open(EXAMPLE_PRODUCTS_PATH, mode='w') as fp:
        json.dump(EXAMPLE_PRODUCTS, fp=fp)

    with open(EXAMPLE_RECIPES_PATH, mode='w') as fp:
        json.dump(EXAMPLE_RECIPES, fp=fp)


def test_load_products_should_return_correct_list_of_products():
    products = EXAMPLE_PRODUCTS

    expected_output = [
        Product(name="egg",
                unit="pieces",
                fat=4.8,
                protein=6.3,
                carbohydrates=0.4),
        Product(name="wholemeal bread",
                unit="g",
                fat=1.7,
                protein=5.9,
                carbohydrates=51.2),
        Product(name="butter",
                unit="g",
                fat=81,
                protein=0.9,
                carbohydrates=0.1)
    ]

    actual_output = load_products(EXAMPLE_PRODUCTS)
    assert actual_output == expected_output
