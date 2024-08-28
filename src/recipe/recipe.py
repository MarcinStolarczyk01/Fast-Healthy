from product.product import Product
from dataclasses import dataclass


@dataclass(frozen=True)
class Recipe:
    name: str
    procedure: list[str]
    products: dict[str:float]
