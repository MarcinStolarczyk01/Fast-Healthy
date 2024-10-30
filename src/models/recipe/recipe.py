from pydantic import BaseModel

from src.food_data_manager.food_data_manager import FoodDataManager


class RecipeModel(BaseModel):
    """
    The example body passed via API:
    {
        "recipe": {
            "name": 'omlet',
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
    def __init__(self, recipe_model: dict):
        recipe_model = RecipeModel(**recipe_model)

        self.name = recipe_model.name
        self.procedure = recipe_model.procedure
        self.products = FoodDataManager.products(tuple(recipe_model.products.keys()))

    def serialize(self) -> dict:  # todo: any usage?
        serialized = {
            "name": self.name,
            "procedure": self.procedure,
            "products": [product.__dict__ for product in self.products],
        }
        return serialized
