import numpy as np

from src.food_data_manager.food_data_manager import FoodDataManager
from pytest import mark

from src.models.product.product import Product


# products nutrients data: https://www.nutritionix.com
@mark.parametrize('requested_product, expected_nutrients', [('cheddar', {'protein': 23,'fat': 33, 'carbohydrates': 3.1}),
                                                           ('chicken breast', {'protein': 23,'fat': 2.6, 'carbohydrates': 0}),
                                                           ('egg', {'protein': 13,'fat': 9.5, 'carbohydrates': 0.7})])
def test_food_data_manager_products_should_return_expected_products(requested_product: str,
                                                                    expected_nutrients: dict[str: float]) -> None:
    manager = FoodDataManager()
    products: tuple[Product, ...] = manager.products(
        [
            requested_product,
        ]
    )

    for product in products:
        for nutrient, value in expected_nutrients:
            assert np.isclose(getattr(product, nutrient, None), value, rtol=0.20)
