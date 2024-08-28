from dataclasses import dataclass

from typing import Optional
from exceptions.exceptions import IncompleteProductInfoError
from keywords.keywords import MacroKeywords

FAT_KCAL = 9
PROTEIN_KCAL = 4
CARBOHYDRATES_KCAL = 4


@dataclass(frozen=True)
class Product:
    name: str

    unit: str
    fat: float | None = None
    protein: float | None = None
    carbohydrates: float | None = None

    def get_kcal(self) -> int:
        if any(
            [
                arg is None
                for arg in [self.unit, self.fat, self.protein, self.carbohydrates]
            ]
        ):
            raise IncompleteProductInfoError(self)
        return int(
            self.fat * FAT_KCAL
            + self.protein * PROTEIN_KCAL
            + self.carbohydrates * CARBOHYDRATES_KCAL
        )

    def get_macro(self) -> dict[str : float | None]:
        return {
            MacroKeywords.fat: self.fat,
            MacroKeywords.protein: self.protein,
            MacroKeywords.carbohydrates: self.carbohydrates,
        }

    @staticmethod
    def incomplete(name: str) -> "Product":
        return Product(name)
