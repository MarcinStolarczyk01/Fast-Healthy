from dataclasses import dataclass


@dataclass(frozen=True, init=False)
class MacroKeywords:
    fat = "fat"
    protein = "protein"
    carbohydrates = "carbohydrates"


@dataclass(frozen=True, init=False)
class ProductsKeywords:
    products = "products"
    name = "name"
    macro = "macro"
    unit = "unit"


@dataclass(frozen=True, init=False)
class UnitKeywords:
    g = "g"
    pieces = "pieces"
    ml = "ml"


@dataclass(frozen=True, init=False)
class RecipeKeywords:
    name = "name"
    products = "products"
    procedure = "procedure"
