from typing import Optional

from pydantic import BaseModel, RootModel


# +------------------+
# |=====Products=====|
# +------------------+
class ProductMacro(BaseModel):
    fat: float
    protein: float
    carbohydrates: float


class Product(BaseModel):
    name: str
    macro: Optional[ProductMacro]
    unit: str


class Products(RootModel):
    root: list[Product]


# +-----------------+
# |=====Recipes=====|
# +-----------------+
class RecipeProducts(RootModel):
    root: dict[str, float]


class RecipeProcedure(RootModel):
    root: list[str]


class Recipe(BaseModel):
    name: str
    products: RecipeProducts
    procedure: RecipeProcedure


class Recipes(BaseModel):
    recipes: list[Recipe]
