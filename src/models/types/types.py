from typing import Literal

from pydantic import BaseModel


# +------------------+
#  =====Products=====
# +------------------+
class ProductMacroType(BaseModel):
    fat: float
    protein: float
    carbohydrates: float


class ProductType(BaseModel):
    name: str
    macro: ProductMacroType
    unit: Literal['g', 'pieces', 'ml', 'l']


class ProductsDBType(BaseModel):
    products: list[ProductType]


# +-----------------+
#  =====Recipes=====
# +-----------------+

class RecipeType(BaseModel):
    name: str
    products: dict[str, float]
    procedure: list[str]


class RecipesDBType(BaseModel):
    recipes: list[RecipeType]
