import numpy as np

from src.food_data_manager.food_data_manager import FoodDataManager
from pytest import mark

from src.models.product.product import Product


# products nutrients data: https://www.nutritionix.com
@mark.parametrize(
    "requested_products, expected_nutrients",
    [
        (
            ["cheddar", "chicken breast raw", "whole egg", "white bread", "rye bread"],
            [
                {"protein": 23, "fat": 33, "carbohydrates": 3.1},
                {"protein": 23, "fat": 2.6, "carbohydrates": 0},
                {"protein": 13, "fat": 9.5, "carbohydrates": 0.7},
                {"protein": 9, "fat": 3, "carbohydrates": 49},
                {"protein": 8.5, "fat": 3.3, "carbohydrates": 48},
            ],
        )
    ],
)
def test_food_data_manager_products_should_return_expected_products(
    requested_products: tuple[str], expected_nutrients: list[dict[str, float]]
) -> None:
    manager = FoodDataManager()
    products: tuple[Product, ...] = manager.products(requested_products)

    for i, product in enumerate(products):
        for nutrient, value in expected_nutrients[i].items():
            assert np.isclose(
                getattr(product, nutrient, None), value, rtol=0.20, atol=3
            )
