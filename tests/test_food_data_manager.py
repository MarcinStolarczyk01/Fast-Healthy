from food_data_manager.food_data_manager import FoodDataManager


def test_food_data_manager_products_should_return_valid_data() -> None:
    manager = FoodDataManager()
    products = manager.products(['cheese cheddar',])
