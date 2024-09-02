from keywords.keywords import RecipeKeywords, ProductsKeywords, MacroKeywords
from models.product.product import Product
from models.recipe.recipe import Recipe
import logging

from models.types import types


def load_products(products: types.Products) -> list[Product]:
    known_products: list[Product] = []
    for product in products:
        macro_section: dict = product[ProductsKeywords.macro]
        known_products.append(
            Product(
                name=product[ProductsKeywords.name],
                unit=product[ProductsKeywords.unit],
                fat=macro_section[MacroKeywords.fat],
                protein=macro_section[MacroKeywords.protein],
                carbohydrates=macro_section[MacroKeywords.carbohydrates],
            )
        )

    return known_products


def load_recipes(recipes: list[dict]) -> list[Recipe]:
    if not recipes:
        logging.debug("Can't load recipes from empty dictionary!")
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
    def __init__(self, recipes_database: list[dict], products_database: list[dict]):
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
