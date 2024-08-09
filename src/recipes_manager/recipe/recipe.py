from product.product import Product


class Recipe:
    def __init__(self, procedure: str, products: dict):
        self.procedure: str = procedure
        self.ingredients: list[Product] = self.load_from_dict(products)

    def load_from_dict(self, ingredients: dict) -> list[Product]:

