import os
import requests
from exceptions.exceptions import MissingAPIKeyError, MissingNutrientError
from models.product.product import Product

API_KEY_NAME = 'FD_CENTRAL_API_KEY'
PROTEIN_ID = 1003
FAT_ID = 1085
CARBOHYDRATES_ID = 1005


class FoodDataManager:
    def __init__(self):
        self.database_api_key = self._get_api_key(API_KEY_NAME)

    def products(self, products_names: list[str]) -> tuple[Product, ...]:
        return [self._search_product(product) for product in products_names]




    def _search_product(self, name: str, data_type: str = 'Foundation,SR%20Legacy', limit: int = 1) -> Product:
        request_url = f"https://api.nal.usda.gov/fdc/v1/foods/search?query={name}&dataType={data_type}&pageSize={limit}&api_key={self.database_api_key}"

        search_results = requests.get(request_url).json()

        foods_section = search_results['foods']
        description = foods_section['description']
        nutrients_section = foods_section['foodNutrients']



    def _find_nutrient_value(self, nut_id: int, nutrients: list[dict]) -> float:
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
