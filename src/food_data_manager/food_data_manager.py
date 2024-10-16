import logging
import os
import time

import requests
from requests import RequestException

from exceptions.exceptions import MissingAPIKeyError, MissingNutrientError, FoodDatabaseConnectionError
from models.product.product import Product
from enum import Enum

API_KEY_NAME = 'FD_CENTRAL_API_KEY'
RETRIES = 5
TIMEOUT = 30
RETRY_PAUSE = 5


class WantedNutrientIDs(Enum):
    protein = 1003
    fat = 1085
    carbohydrates = 1005


class FoodDataManager:
    def __init__(self):
        self.database_api_key = self._get_api_key(API_KEY_NAME)
        self.api_endpoint = 'https://api.nal.usda.gov/fdc/v1/foods/search'

    def products(self, products_names: list[str]) -> tuple[Product, ...]:
        return tuple(self._search_product(name) for name in products_names)

    def _search_product(self, name: str, data_type: str = 'Foundation,SR%20Legacy', limit: int = 1) -> Product:
        request_url = f"{self.api_endpoint}?query={name}&dataType={data_type}&pageSize={limit}&api_key={self.database_api_key}"

        fails = 0
        while True:
            try:
                search_results = requests.get(request_url, timeout=TIMEOUT).json()
                break
            except RequestException as e:
                fails += 1
                if fails == RETRIES:
                    raise FoodDatabaseConnectionError(
                        f'Can not establish connection with usda food database {self.api_endpoint}. More info about the error: {e}')

                for sec in reversed(range(1, RETRY_PAUSE + 1)):
                    logging.info(f"Retrying database request in {sec} sec...")
                    time.sleep(1)

        foods_section = search_results['foods']
        food = foods_section[0]
        found_product_name = food['description']
        nutrients_section: list[dict] = food['foodNutrients']
        nutrients = {nutrient.name: self._find_nutrient_value(nutrient.value, nutrients_section) for nutrient in
                     WantedNutrientIDs}
        return Product(found_product_name, nutrients=nutrients)

    @staticmethod
    def _find_nutrient_value(nut_id: int, nutrients: list[dict]) -> float:
        for nutrient in nutrients:
            if nutrient["nutrientId"] == nut_id:
                return nutrient['value']

        raise MissingNutrientError(f"Nutrient under id: {nut_id} not present in search results")

    @staticmethod
    def _get_api_key(variable: str) -> str:
        try:
            return os.environ[variable]
        except KeyError:
            raise MissingAPIKeyError(f"Can't find environmental variable under the name: {variable}. \n\
                                       Can't query products from the database.")
