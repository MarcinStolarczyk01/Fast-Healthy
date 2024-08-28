from pathlib import Path

from files_io.files_io import open_json

# from product.product import Product
# from recipe.recipe import Recipe
from database_manager.database_manager import DataBaseManager


def test_():
    recipes: dict = open_json(
        file_path=Path(__file__)
        .parents[1]
        .joinpath("src/database_manager/database/recipes.json")
    )

    products: dict = open_json(
        file_path=Path(__file__)
        .parents[1]
        .joinpath("src/database_manager/database/products.json")
    )

    db_mgr = DataBaseManager(recipes["recipes"], products["products"])
