from pydantic import BaseModel

from src.food_data_manager.food_data_manager import FoodDataManager


class RecipeModel(BaseModel):
    name: str
    procedure: tuple[str, ...]
    products: dict[str, float]


class Recipe:
    def __init__(self, recipe_model: RecipeModel):
        self.name = recipe_model.name
        self.procedure = recipe_model.procedure
        self.products = FoodDataManager.products(tuple(recipe_model.products.keys()))

    @property
    def kcal(self) -> int:
        return sum(product.kcal for product in self.products)
