from keywords.keywords import RecipeKeywords, ProductsKeywords, MacroKeywords
from models.product.product import Product
from models.recipe.recipe import Recipe
import logging

from models.types.types import ProductsDBType, RecipesDBType


def load_products(products_db: ProductsDBType) -> list[Product]:
    known_products: list[Product] = []
    for product in products_db.products:
        known_products.append(
            Product(
                name=product.name,
                unit=product.unit,
                fat=product.macro.fat,
                protein=product.macro.protein,
                carbohydrates=product.macro.carbohydrates,
            )
        )

    return known_products


def load_recipes(recipes: RecipesDBType) -> list[Recipe]:
    known_recipes: list[Recipe] = [
        Recipe(
            name=recipe[RecipeKeywords.name],
            procedure=recipe[RecipeKeywords.procedure],
            products=recipe[RecipeKeywords.products],
        )
        for recipe in recipes
    ]

    return known_recipes


class DataBaseManager:
    def __init__(self, recipes_database: RecipesDBType, products_database: ProductsDBType):
        self.known_products: list[Product] = load_products(products_database)
        self.known_recipes: list[Recipe] = load_recipes(recipes_database)

    def find_product(self, name: str) -> Product | None:
        for product in self.known_products:
            if product.name == name:
                return product
        logging.warning(
            f"Product {name} not present in database. \
        Add product information to enable using it in your recipes!"
        )
