from dataclasses import dataclass


@dataclass(frozen=True, init=False)
class MacroKeywords:
    macro = "macro"
    fat = "fat"
    protein = "protein"
    carbohydrates = "carbohydrates"


@dataclass(frozen=True, init=False)
class ProductsKeywords:
    products = "products"
    egg = "egg"
    wholemeal_bread = "wholemeal bread"
    butter = "butter"


@dataclass(frozen=True, init=False)
class UnitKeywords:
    g = "g"
    pieces = "pieces"
    ml = "ml"
