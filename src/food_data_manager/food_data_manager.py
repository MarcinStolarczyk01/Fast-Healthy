import logging
import os
import threading
import time
import requests
from pydantic import BaseModel
from requests import RequestException
from enum import Enum
from concurrent.futures import ThreadPoolExecutor

from src.exceptions.exceptions import (
    MissingAPIKeyError,
    MissingNutrientError,
    FoodDatabaseConnectionError,
)
from src.models.product.product import Product


class WantedNutrientIDs(Enum):
    protein = 1003
    fat = 1004
    carbohydrates = 1005


class ResponseNutrient(BaseModel):
    nutrientId: int
    value: float


class ResponseFoodModel(BaseModel):
    description: str
    foodNutrients: list[ResponseNutrient]


class ResponseModel(BaseModel):
    foods: list[ResponseFoodModel]


def _get_api_key(variable: str) -> str:
    try:
        return os.environ[variable]
    except KeyError:
        raise MissingAPIKeyError(
            f"Can't find environmental variable under the name: {variable}. \n\
                                   Can't query products from the database."
        )


def _find_nutrient_value(nut_id: int, nutrients: list[ResponseNutrient]) -> float:
    for nutrient in nutrients:
        if nutrient.nutrientId == nut_id:
            return nutrient.value

    raise MissingNutrientError(
        f"Nutrient under id: {nut_id} not present in search results"
    )


class FoodDataManager:
    API_KEY_NAME = "FD_CENTRAL_API_KEY"

    DATABASE_API_KEY = _get_api_key(API_KEY_NAME)
    API_ENDPOINT = "https://api.nal.usda.gov/fdc/v1/foods/search"

    RETRIES = 5
    TIMEOUT = 30
    RETRY_PAUSE = 5

    @classmethod
    def products(cls, products_names: tuple[str, ...]) -> tuple[Product, ...]:
        products = []
        with ThreadPoolExecutor(max_workers=100) as executor:
            products.extend(executor.map(cls._search_product, products_names))
        return tuple(products)

    @classmethod
    def _search_product(
        cls, name: str, data_type: str = "Foundation,SR%20Legacy", limit: int = 1
    ) -> Product:
        request_url = f"{cls.API_ENDPOINT}?query={name}&dataType={data_type}&pageSize={limit}&api_key={cls.DATABASE_API_KEY}"

        fails = 0
        while True:
            try:
                response = requests.get(request_url, timeout=cls.TIMEOUT)
                response.raise_for_status()
                search_results = response.json()
                break
            except RequestException as e:
                fails += 1
                if fails == cls.RETRIES:
                    raise FoodDatabaseConnectionError(
                        f"Cannot establish connection with USDA food database at {cls.API_ENDPOINT}. "
                        f"More info about the error: {e}"
                    )
                logging.info(f"Retrying database request in {cls.RETRY_PAUSE} sec...")
                time.sleep(cls.RETRY_PAUSE)

        search_results = ResponseModel(**search_results)

        foods_section = search_results.foods
        food = foods_section[0]
        found_product_name = food.description
        nutrients_section = food.foodNutrients
        nutrients = {
            nutrient.name: _find_nutrient_value(nutrient.value, nutrients_section)
            for nutrient in WantedNutrientIDs
        }
        return Product(found_product_name, nutrients=nutrients)
