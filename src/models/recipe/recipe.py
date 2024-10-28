from dataclasses import dataclass
from itertools import product

from pydantic import BaseModel

from food_data_manager.food_data_manager import FoodDataManager
from models.product.product import Product


class RecipeModel(BaseModel):
    """
    The body passed via API:
    {
        "recipe": {
            "name": string,
            "procedure": [
                "Make something",
                "Make something else",
                "Finish"
            ],
            "products": {
                "egg": 3,
                "butter": 10
            }
        }
    }
    """

    name: str
    procedure: tuple[str, ...]
    products: dict[str, float]


class Recipe:
    def __init__(self, recipe_model: RecipeModel):
        self.name: str = recipe_model.name
        self.procedure: tuple[str, ...] = recipe_model.procedure
        product_names = tuple(product_name for product_name in recipe_model.products)
        self.products: dict[Product, float] = {
            FoodDataManager.products(recipe_model.products)
        }  # todo
