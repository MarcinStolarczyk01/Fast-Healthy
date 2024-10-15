import os
import requests
from exceptions.exceptions import MissingAPIKeyError, MissingNutrientError
from models.product.product import Product
from enum import Enum

API_KEY_NAME = 'FD_CENTRAL_API_KEY'


class WantedNutrientIDs(Enum):
    PROTEIN = 1003
    FAT = 1085
    CARBOHYDRATES_ID = 1005


class FoodDataManager:
    def __init__(self):
        self.database_api_key = self._get_api_key(API_KEY_NAME)
        self.api_endpoint = 'https://api.nal.usda.gov/fdc/v1/foods/search'

    def products(self, products_names: list[str]) -> tuple[Product, ...]:
        return tuple(self._search_product(name) for name in products_names)

    def _search_product(self, name: str, data_type: str = 'Foundation,SR%20Legacy', limit: int = 1) -> Product:
        request_url = f"{self.api_endpoint}?query={name}&dataType={data_type}&pageSize={limit}&api_key={self.database_api_key}"

        search_results = requests.get(request_url).json()

        foods_section = search_results['foods']
        name = foods_section['description']
        nutrients_section: list[dict] = foods_section['foodNutrients']
        nutrients = {nutrient.name: self._find_nutrient_value(nutrient.value, nutrients_section) for nutrient in
                     WantedNutrientIDs}
        return Product(name, nutrients)

    @staticmethod
    def _find_nutrient_value(nut_id: int, nutrients: list[dict]) -> float:
        for nutrient in nutrients:
            if nutrient["nutrientId"] == nut_id:
                return nutrient['value']

        raise MissingNutrientError(f"Nutrient under id: {nut_id} not present in search results")

    @staticmethod
    def _get_api_key(variable_name: str) -> str:
        try:
            return os.environ[variable_name]
        except KeyError:
            raise MissingAPIKeyError(f"Can't find environmental variable under the name: {variable_name}. \n\
                                       Can't query products from the database.")
